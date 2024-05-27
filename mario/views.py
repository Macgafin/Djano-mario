from django.shortcuts import render
from .models import PlayVideo, ClearValue, Script, Feedback
import os
from django.conf import settings

# Create your views here.

def home(request):
    videos = PlayVideo.objects.all()
    clear_values = ClearValue.objects.all()
    scripts = Script.objects.all()
    feedbacks = Feedback.objects.all()
    
    # ビデオファイルのパスを設定
    video_file_path = os.path.join(settings.STATIC_ROOT, 'mario/Screen information/stage 1 short vr.mp4')
    
    return render (request, "mario/home.html",{
        'videos': videos,
        'clear_values': clear_values,
        'scripts': scripts,
        'feedbacks': feedbacks
    })

def information(request, video_name):
    game_info = []  # ゲーム情報を格納するリスト

    # テキストファイルの数を取得
    num_text_files = 100  # テキストファイルの数に合わせて設定してください

    # 各テキストファイルから情報を読み取る
    for i in range(1, num_text_files + 1):
        text_file_path = f'mario/Screen information/discrimination result/stage 1 short vr_{i}.txt'
        with open(text_file_path, 'r') as file:
            for line in file:
                # 行を空白で分割して、各要素をリストに追加
                data = line.strip().split()
                # 信頼値を除いた最初の4つの要素を抽出してリストに追加
                game_info.append(data[:4])

    return render(request, 'mario/home.html', {'game_info': game_info})

