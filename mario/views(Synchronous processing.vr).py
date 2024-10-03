from django.shortcuts import render
from .models import PlayVideo, ClearValue, Script, OurFeedback, PlayerFeedback
import os
from django.conf import settings
from pathlib import Path
import logging
import time
from .viewservices import process_game_info
from django.http import StreamingHttpResponse
from .rta_sub import video_stream
from django.views.decorators.csrf import csrf_exempt



def home(request):
    clear_values = ClearValue.objects.all()
    scripts = Script.objects.all()
    ourfeedbacks = OurFeedback.objects.all()

    # ビデオファイルのパスを設定
    video_file_path = os.path.join(settings.STATIC_URL, 'mario_django/mainproject/mario/realtime_detection.mp4')

    # ゲーム情報を格納するリスト
    game_info = []

    # 設定からコードとテキストのマッピングを取得
    code_texts = settings.CODE_TEXTS

    # 読み込むテキストファイルのパスを設定 /// 'mario_django' / 'mainproject'
    text_file_path = Path(settings.BASE_DIR)  / 'mario' / 'static' / 'mario' / 'realtime_analytics.txt'
    
    if text_file_path.exists():
        with open(text_file_path, 'r') as file:
            for line in file:
                data = line.strip().split()
                if len(data) >= 6 and data[0] in code_texts:
                    game_info.append({
                        'code': code_texts[data[0]],
                        'x': float(data[1]),
                        'y': float(data[2]),
                        'width': float(data[3]),
                        'height': float(data[4]),
                        'confidence': float(data[5]),  # 信頼度
                        'timestamp': float(data[6]),  # タイムスタンプ
                    })
    else:
        logging.warning(f'File not found: {text_file_path}')
        
    # 現在時刻を記録
    current_time = time.time()
    # サービス層の関数を呼び出す
    scripts = process_game_info(game_info, current_time)

    return render(request, "mario/home.html", {
        'clear_values': clear_values,
        'scripts': scripts,
        'ourfeedbacks': ourfeedbacks,
        'game_info': game_info, #ゲーム情報のテンプレート
        'video_file_path': video_file_path,  # 動画ファイルパスを渡す
    })


#フィードバックのより詳しい説明のページ
def image_details(request):
    game_info = []  # ゲーム情報を格納するリスト
    
    return render(request, 'mario/image_details.html', {'game_info': game_info})

@csrf_exempt
async def stream_view(request):
    return StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')