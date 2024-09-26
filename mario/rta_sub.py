import cv2
from pathlib import Path
from ultralytics import YOLO
import time

# モデルのパス
model_path = Path(__file__).resolve().parent / 'static/mario/best.pt'
text_output_path = Path(__file__).resolve().parent / 'static/mario/realtime_analytics.txt'

# YOLOv8モデルをロード
model = YOLO(model_path)

def video_stream():
    # OBSの仮想カメラから映像をキャプチャ
    cap = cv2.VideoCapture(2)  # 仮想カメラのIDが2と仮定

    if not cap.isOpened():
        print("Error: カメラが開けませんでした")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # YOLOで画像検出
            results = model(frame)

            # 検出結果をテキストファイルに保存
            with open(text_output_path, 'w') as f:
                for result in results:
                    for box in result.boxes:
                        cls = int(box.cls[0])  # クラスID
                        conf = box.conf[0]  # 信頼度
                        x, y, w, h = box.xywh[0]  # バウンディングボックスの座標とサイズ
                        timestamp = time.time()  # 検出時間
                        f.write(f'{cls} {x} {y} {w} {h} {conf} {timestamp}\n')

                        # バウンディングボックスをフレームに描画
                        cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
                        cv2.putText(frame, f'Class: {cls}, Conf: {conf:.2f}', (int(x), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # フレームをJPEG形式にエンコード
            _, buffer = cv2.imencode('.jpg', frame)

            # ストリーミング用にフレームを送信
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            print("Error: フレームをキャプチャできませんでした")
            break

    cap.release()
