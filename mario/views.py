import os
import time
from pathlib import Path
import aiofiles
from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import render
from .models import ClearValue, Script, OurFeedback
from .rta_sub import video_stream  # 非同期対応したストリーミング関数をimport
from .viewservices import process_game_info
from django.views.decorators.csrf import csrf_exempt
import asyncio
import logging
from channels.layers import get_channel_layer
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .forms import QuestionnaireForm


# ロガーを設定
logger = logging.getLogger(__name__)

# ゲーム情報ファイルを非同期で読み込む
async def read_game_info_file(file_path, code_texts):
    game_info = []
    try:
        if file_path.exists():
            async with aiofiles.open(file_path, "r") as file:
                async for line in file:
                    data = line.strip().split()
                    if len(data) >= 6 and data[0] in code_texts:
                        game_info.append({
                            "code": code_texts[data[0]],
                            "x": float(data[1]),
                            "y": float(data[2]),
                            "width": float(data[3]),
                            "height": float(data[4]),
                            "confidence": float(data[5]),
                            "timestamp": float(data[6]),
                        })
        else:
            logger.error(f"File not found: {file_path}")
            game_info.append({"error": "ファイルが見つかりません。"})
    except Exception as e:
        logger.exception("Error reading the game info file.")
        game_info.append({"error": "ゲーム情報の読み込み中にエラーが発生しました。"})

    return game_info

# フィードバックを非同期でファイルに書き込む
async def write_feedback_to_file(feedback_message):
    feedback_file_path = Path(settings.BASE_DIR) / "mario" / "static" / "mario" / "feedback.txt"
    try:
        async with aiofiles.open(feedback_file_path, "w", encoding="utf-8") as file:
            await file.write(f"{feedback_message}\n")
        logger.info("Feedback written to feedback.txt")
    except Exception as e:
        logger.error(f"Error writing to feedback.txt: {e}")

# WebSocketメッセージを送信する
async def send_message_to_websocket(channel_layer, message_type, message):
    try:
        await channel_layer.group_send(
            "game_info",
            {
                "type": message_type,
                "message": message,
            },
        )
        logger.info(f"Message '{message_type}' sent successfully")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

# ホームビューを非同期化
async def home(request):
    # 非同期でデータベースとゲーム情報ファイルを読み込む
    clear_values = await asyncio.to_thread(ClearValue.objects.all)
    scripts = await asyncio.to_thread(Script.objects.all)
    ourfeedbacks = await asyncio.to_thread(OurFeedback.objects.all)
    
    #設定のcode_textsを読み込み
    code_texts = settings.CODE_TEXTS
    text_file_path = Path(settings.BASE_DIR) / "mario" / "static" / "mario" / "realtime_analytics.txt"
    
    # WebSocketにゲーム情報を送信
    game_info = await read_game_info_file(text_file_path, code_texts)
    channel_layer = get_channel_layer()
    await send_message_to_websocket(channel_layer, "send_game_info", game_info)

    # ゲーム情報を処理してフィードバックを生成
    current_time = time.time()
    feedback_message = None
    scripts = process_game_info(game_info, current_time)

    # フィードバックが「巻き戻し中！」や「問題なし」でない場合にファイルに書き込む
    if scripts and scripts not in ["巻き戻し中！", "問題なし"]:
        feedback_message = scripts
        #関数を呼び出してfeedback.txtに書き込む
        await write_feedback_to_file(feedback_message)

    # collision_messageをWebSocket経由で送信
    await send_message_to_websocket(channel_layer, "send_collision_message", feedback_message)

    # レンダリングしてレスポンスを返す
    return render(
        request,
        "mario/home.html",
        {
            "clear_values": clear_values,
            "scripts": scripts,
            "ourfeedbacks": ourfeedbacks,
            "game_info": game_info,
            "video_file_path": os.path.join(settings.STATIC_URL, "mario_django/mainproject/mario/realtime_detection.mp4"),
        },
    )


# 　パスなどのメモ一応残しとく
# MEMO_PATH = os.path.join(settings.BASE_DIR, 'mainproject', 'mario', 'static', 'mario', 'memo.txt')
# QUESTIONNAIRE_PATH = os.path.join(settings.BASE_DIR, 'mainproject', 'mario', 'static', 'mario', 'questionnaire.txt')
@csrf_exempt
async def stream_view(request):
    response = StreamingHttpResponse(
        video_stream(), content_type="multipart/x-mixed-replace; boundary=frame"
    )
    return response


# フィードバックのより詳しい説明のページ
def image_details(request):
    game_info = []  # ゲーム情報を格納するリスト
    return render(request, "mario/image_details.html", {"game_info": game_info})


# 質問フォームの処理
def questionnaire(request):
    if request.method == "POST":
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            # 同期的にファイルに書き込む
            with open("mario/static/mario/questionnaire.txt", "a", encoding="utf-8") as f:
                f.write("ゲーム進行のスムーズさ: {}\n".format(form.cleaned_data["game_progression"]))
                f.write("フィードバックの有用性: {}\n".format(form.cleaned_data["feedback_usefulness"]))
                f.write("学習効果: {}\n".format(form.cleaned_data["learning_effect"]))
                f.write("進捗効果: {}\n".format(form.cleaned_data["learning_progress"]))
                f.write("組み合わせ: {}\n".format(form.cleaned_data["learning_combination"]))
                f.write("システムの使いやすさ: {}\n".format(form.cleaned_data["system_usability"]))
                f.write("システム利用しての総合評価: {}\n".format(form.cleaned_data["overall_experience"]))
                f.write("発展性評価: {}\n".format(form.cleaned_data["System_Development"]))
                f.write("システム前の状態: {}\n".format(form.cleaned_data["pre_system_feedback"]))
                f.write("システム利用後の状態: {}\n".format(form.cleaned_data["post_system_feedback"]))
                f.write("システム利用の感想: {}\n".format(form.cleaned_data["feedback"]))
                f.write("改善点: {}\n".format(form.cleaned_data["suggestions"]))
                f.write("-" * 40 + "\n")  # 区切り線

            # フォームをリセットして確認メッセージを表示
            form = QuestionnaireForm()  # 空のフォームを再生成
            return render(request, "mario/home.html", {"form": form})  # 送信後にThank youページを表示

    else:
        form = QuestionnaireForm()

    return render(request, "mario/questionnaire.html", {"form": form})


# フィードバックを保存する処理
@csrf_exempt
def submit_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get("feedback", "")
        if feedback:
            # 同期的にファイルに書き込む
            with open("mario/static/mario/memo.txt", "a", encoding="utf-8") as file:
                file.write(f"{feedback}\n")
    return redirect("/")


# 経験を保存する処理
@csrf_exempt
def submit_experience(request):
    if request.method == "POST":
        experience = request.POST.get("experience", "")
        if experience:
            # 同期的にファイルに書き込む
            with open(
                "mario/static/mario/questionnaire.txt", "a", encoding="utf-8"
            ) as file:
                file.write(f"{experience}\n")
    return redirect("/")
