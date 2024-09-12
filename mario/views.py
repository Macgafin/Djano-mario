from django.shortcuts import render
from .models import PlayVideo, ClearValue, Script, OurFeedback, PlayerFeedback
import os
from django.conf import settings
from pathlib import Path
import logging
import time
from .viewservices import process_game_info
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

    # 各コードに対応するテキスト
    code_texts = {
        '0': 'Small Mario ：',
        '1': 'Big Mario ：',
        '2': 'Fire Mario ：',
        '3': 'Fish  ：',
        '4': 'Nokonoko  ：',
        '5': 'Coin ：',
        '6': 'Kuribo  ：',
        '7': 'Hatena Block：',
        '8': 'Kinoko ：',
        '9': 'Scaffold ：',
        '10': 'Pipe ：',
        '11': 'P Flower ：',
        '12': 'Togezo ：',
        '13': 'Mario S to B ：',
        '14': 'Star Mario ：',
        '15': 'Star ：',
    }

    # 読み込むテキストファイルのパスを設定
    text_file_path = Path(settings.BASE_DIR) / 'mario' / 'static' / 'mario' / 'discrimination_result' / 'stage 1 short vr_1.txt'
    
    if text_file_path.exists():
        with open(text_file_path, 'r') as file:
            for line in file:
                # 行を空白で分割して、各要素をリストに追加
                data = line.strip().split()
                # 信頼値を除いた最初の5つの要素を抽出してリストに追加
                if len(data) >= 5 and data[0] in code_texts:
                    game_info.append({
                        'code': code_texts[data[0]],
                        'x': float(data[1]),  # 数値に変換
                        'y': float(data[2]),  # 数値に変換
                        'width' : float(data[3]),  # 数値に変換
                        'height': float(data[4]),  # 数値に変換
                        
                    })
    else:
        logging.warning(f'File not found: {text_file_path}')
        
    # 現在時刻を記録
    current_time = time.time()
    # サービス層の関数を呼び出す
    scripts = process_game_info(game_info, current_time)

    return render(request, "mario/home.html", {
        'videos': videos,
        'clear_values': clear_values,
        'scripts': scripts,
        'ourfeedbacks': ourfeedbacks,
        'playerfeedbacks': playerfeedbacks,
        'game_info': game_info,  # ゲーム情報をテンプレートに渡す
    })


#フィードバックのより詳しい説明のページ
def image_details(request):
    game_info = []  # ゲーム情報を格納するリスト
    
    return render(request, 'mario/image_details.html', {'game_info': game_info})

# YOLO を読み込む要コード
# def home(request):
#     videos = PlayVideo.objects.all()
#     clear_values = ClearValue.objects.all()
#     scripts = Script.objects.all()
#     ourfeedbacks = OurFeedback.objects.all()
#     playerfeedbacks = PlayerFeedback.objects.all()

#     # ビデオファイルのパスを設定
#     video_file_path = os.path.join(settings.STATIC_ROOT, 'mario/Screen information/stage 1 short vr.mp4')

#     # ゲーム情報を格納するリスト
#     game_info = []

#     # 各コードに対応するテキスト
#     code_texts = {
#         '0': 'Small Mario は ({}, {}) にいます。',
#         '1': 'Big Mario は ({}, {}) にいます。',
#         '2': 'Fire Mario は ({}, {}) にいます。',
#         '3': 'Fish は ({}, {}) にいます。',
#         '4': 'Nokonoko は ({}, {}) にいます。',
#         '5': 'Coin は ({}, {}) にあります。',
#         '6': 'Kuribo は ({}, {}) にいます。',
#         '7': 'Hatena Block は ({}, {}) にあります。',
#         '8': 'Kinoko は ({}, {}) にいます。',
#         '9': 'Scaffold は ({}, {}) にあります。',
#         '10': 'Pipe は ({}, {}) にあります。',
#         '11': 'P Flower は ({}, {}) にあります。',
#         '12': 'Togezo は ({}, {}) にいます。',
#         '13': 'Mario S to B は ({}, {}) にいます。',
#         '14': 'Star Mario は ({}, {}) にいます。',
#         '15': 'Star は ({}, {}) にあります。',
#     }

#     # テキストファイルのディレクトリを設定
#     text_files_dir = Path(settings.BASE_DIR) / 'mario' / 'static' / 'mario' / 'discrimination_result'
#     text_files = sorted(text_files_dir.glob('stage 1 short vr_*.txt'), key=lambda x: x.name)

#     # 各テキストファイルから情報を読み取る
#     for text_file_path in text_files:
#         if text_file_path.exists():
#             with open(text_file_path, 'r') as file:
#                 for line in file:
#                     # 行を空白で分割して、各要素をリストに追加
#                     data = line.strip().split()
#                     # 信頼値を除いた最初の4つの要素を抽出してリストに追加
#                     if len(data) >= 3 and data[0] in code_texts:
#                         game_info.append(code_texts[data[0]].format(data[1], data[2]))
#         else:
#             logging.warning(f'File not found: {text_file_path}')

#     return render(request, "mario/home.html", {
#         'videos': videos,
#         'clear_values': clear_values,
#         'scripts': scripts,
#         'ourfeedbacks': ourfeedbacks,
#         'playerfeedbacks': playerfeedbacks,
#         'game_info': game_info,  # ゲーム情報をテンプレートに渡す
#         'code_texts': code_texts, # 各コードに対応するテキストをテンプレートに渡す
#     })
