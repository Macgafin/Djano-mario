import cv2
import time
from pathlib import Path
from ultralytics import YOLO
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import StreamingHttpResponse
import aiofiles
import asyncio
import logging

# モデルのパス
model_path = Path(__file__).resolve().parent / 'static/mario/mario-nomal.pt'
text_output_path = Path(__file__).resolve().parent / 'static/mario/realtime_analytics.txt'

# ログレベルをWARNINGに設定することで、INFOレベルの出力を抑制
logging.getLogger('ultralytics').setLevel(logging.WARNING)
# YOLOv8モデルをロード
model = YOLO(model_path)


# 非同期ストリーミング関数
async def video_stream():
    # OBSの仮想カメラから映像をキャプチャ
    cap = cv2.VideoCapture(1)  # 仮想カメラのIDが2と仮定

    if not cap.isOpened():
        print("Error: カメラが開けませんでした")
        return

    channel_layer = get_channel_layer()  # チャンネルレイヤを取得

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            
            # YOLOで画像検出（非同期処理）
            results = await asyncio.to_thread(model, frame)

            # 検出結果を非同期でテキストファイルに保存し、game_infoに追加
            async with aiofiles.open(text_output_path, 'w') as f:
                for result in results:
                    for box in result.boxes:
                        cls = int(box.cls[0])  # クラスID
                        conf = box.conf[0]  # 信頼度
                        x, y, w, h = box.xywh[0]  # バウンディングボックスの座標とサイズ
                        timestamp = time.time()  # 検出時間
                        await f.write(f'{cls} {x} {y} {w} {h} {conf} {timestamp}\n')

                        # バウンディングボックスをフレームに描画
                        cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
                        cv2.putText(frame, f'Class: {cls}, Conf: {conf:.2f}', (int(x), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


            # フレームをJPEG形式にエンコード（非同期対応）
            _, buffer = await asyncio.to_thread(cv2.imencode, '.jpg', frame)

            # ストリーミング用にフレームを送信
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            print("Error: フレームをキャプチャできませんでした")
            break

    cap.release()
