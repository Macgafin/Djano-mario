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

# ホームビューを非同期化
async def home(request):
    clear_values = await asyncio.to_thread(ClearValue.objects.all)
    scripts = await asyncio.to_thread(Script.objects.all)
    ourfeedbacks = await asyncio.to_thread(OurFeedback.objects.all)

    # 動画ファイルパス
    video_file_path = os.path.join(settings.STATIC_URL, 'mario_django/mainproject/mario/realtime_detection.mp4')

    # ゲーム情報
    game_info = []
    
    # 設定からコードとテキストのマッピングを取得
    code_texts = settings.CODE_TEXTS
    
    # 読み込むテキストファイルのパスを設定
    text_file_path = Path(settings.BASE_DIR) / 'mario' / 'static' / 'mario' / 'realtime_analytics.txt'

    # 非同期でファイルの読み込みを行う
    try:
        if text_file_path.exists():
            async with aiofiles.open(text_file_path, 'r') as file:
                async for line in file:
                    data = line.strip().split()
                    if len(data) >= 6 and data[0] in code_texts:
                        game_info.append({
                            'code': code_texts[data[0]],
                            'x': float(data[1]),
                            'y': float(data[2]),
                            'width': float(data[3]),
                            'height': float(data[4]),
                            'confidence': float(data[5]),
                            'timestamp': float(data[6]),
                        })
        else:
            logger.error(f'File not found: {text_file_path}')
            # クライアントにエラーメッセージを送信することも考慮できます
            game_info.append({'error': 'ファイルが見つかりません。'})

    except Exception as e:
        logger.exception('Error reading the game info file.')
        game_info.append({'error': 'ゲーム情報の読み込み中にエラーが発生しました。'})

    # WebSocketにゲーム情報を送信する
    channel_layer = get_channel_layer()
    
    
    print("start print game_info")
    print(game_info)  # game_infoの内容を確認
    print("end print game_info")

    try:
        logger.info("Sending game_info to consumers.py")
        await channel_layer.group_send(
            'game_info',
            {
                'type': 'send_game_info',  # receiveメソッドで処理するために'type'を指定
                'message': game_info
            }
        )
        logger.info("Game info sent successfully")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        
        
    # 現在時刻を記録
    current_time = time.time()
    # サービス層の関数を呼び出す
    scripts = process_game_info(game_info, current_time)

    return render(request, "mario/home.html", {
        'clear_values': clear_values,
        'scripts': scripts,
        'ourfeedbacks': ourfeedbacks,
        'game_info': game_info,
        'video_file_path': video_file_path,
    })

#　パスなどのメモ一応残しとく
# MEMO_PATH = os.path.join(settings.BASE_DIR, 'mainproject', 'mario', 'static', 'mario', 'memo.txt')
# QUESTIONNAIRE_PATH = os.path.join(settings.BASE_DIR, 'mainproject', 'mario', 'static', 'mario', 'questionnaire.txt')
@csrf_exempt
async def stream_view(request):
    response = StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response

# フィードバックのより詳しい説明のページ
def image_details(request):
    game_info = []  # ゲーム情報を格納するリスト
    return render(request, 'mario/image_details.html', {'game_info': game_info})

async def questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            async with aiofiles.open('mainproject/mario/static/mario/questionnaire.txt', 'a') as f:
                await f.write("システム利用しての総合評価: " + form.cleaned_data['rating_experience'] + "\n")
                await f.write("システムの使いやすさ: " + form.cleaned_data['rating_usability'] + "\n")
                await f.write("作業効率への効果: " + form.cleaned_data['rating_efficiency'] + "\n")
                await f.write("システム利用時と未使用時の違い: " + form.cleaned_data['rating_comparison'] + "\n")
                await f.write("システム利用の感想: " + form.cleaned_data['feedback'] + "\n")
                await f.write("改善点: " + form.cleaned_data['suggestions'] + "\n\n")
            return redirect('home')  # 送信後にホームページへリダイレクト
    else:
        form = QuestionnaireForm()
    return render(request, 'mario/questionnaire.html', {'form': form})

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback', '')
        if feedback:
            # 'w' モードでファイルを開き、上書き保存
            with open('mario/static/mario/memo.txt', 'a', encoding='utf-8') as file:
                file.write(f"{feedback}\n")
    return redirect('/')

@csrf_exempt
def submit_experience(request):
    if request.method == 'POST':
        experience = request.POST.get('experience', '')
        if experience:
            with open('mario/static/mario/questionnaire.txt', 'a', encoding='utf-8') as file:
                file.write(f"{experience}\n")
    return redirect('/')
