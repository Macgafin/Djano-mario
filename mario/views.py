from django.shortcuts import render
from .models import PlayVideo, ClearValue, Script, OurFeedback, PlayerFeedback
import os
from django.conf import settings
from pathlib import Path
import logging

# Create your views here.

def home(request):
    videos = PlayVideo.objects.all()
    clear_values = ClearValue.objects.all()
    scripts = Script.objects.all()
    ourfeedbacks = OurFeedback.objects.all()
    playerfeedbacks = PlayerFeedback.objects.all()
    
    # ビデオファイルのパスを設定
    video_file_path = os.path.join(settings.STATIC_ROOT, 'mario/Screen information/stage 1 short vr.mp4')
    
    # ゲーム情報を格納するリスト
    game_info = []

    # テキストファイルの数を設定
    num_text_files = 100  # テキストファイルの数に合わせて設定してください
    
    # 各テキストファイルから情報を読み取る
    for i in range(1, num_text_files + 1):
        text_file_path = Path(settings.BASE_DIR) / 'mario' / 'static' / 'mario' / 'discrimination_result' / f'stage 1 short vr_{i}.txt'
        if text_file_path.exists():
            with open(text_file_path, 'r') as file:
                for line in file:
                    # 行を空白で分割して、各要素をリストに追加
                    data = line.strip().split()
                    # 信頼値を除いた最初の4つの要素を抽出してリストに追加
                    game_info.append([data[0], data[1], data[2]])
                    
        else:
            logging.warning(f'File not found: {text_file_path}')

    
    return render (request, "mario/home.html",{
        'videos': videos,
        'clear_values': clear_values,
        'scripts': scripts,
        'ourfeedbacks': ourfeedbacks,
        'playerfeedbacks': playerfeedbacks,
        'game_info': game_info,  # ゲーム情報をテンプレートに渡す
        
    })

def image_details(request):
    game_info = []  # ゲーム情報を格納するリスト
    
    return render(request, 'mario/image_details.html', {'game_info': game_info})

