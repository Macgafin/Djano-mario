import cv2
from ultralytics import YOLO
from pathlib import Path
import time

# スクリプトのディレクトリを取得
script_dir = Path(__file__).resolve().parent

# YOLOv8のモデルを読み込む
model_path = script_dir / 'best.pt'
model = YOLO(model_path)

# OBSの仮想カメラから映像をキャプチャ
cap = cv2.VideoCapture(2)  # 仮想カメラのIDが2と仮定

# 保存先の動画ファイルパスを設定
video_output_path = script_dir / 'realtime_detection.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(str(video_output_path), fourcc, fps, (width, height))

# テキストファイルのパス
text_output_path = script_dir / 'realtime_analitics.txt'

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # YOLOv8でフレームを解析
        results = model(frame)

        # 検出結果をフレームに描画
        annotated_frame = results[0].plot()

        # 処理後のフレームを動画ファイルに書き出す
        out.write(annotated_frame)

        # 検出結果をテキストファイルに保存
        with open(text_output_path, 'w') as f:
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])  # クラスID
                    conf = box.conf[0]  # 信頼度
                    x, y, w, h = box.xywh[0]  # バウンディングボックスの座標とサイズ
                    timestamp = time.time()  # 検出時間
                    f.write(f'{cls} {x} {y} {w} {h} {conf} {timestamp}\n')

        # 終了条件 (例えば 'q' キーで終了)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


# リソースを解放
cap.release()
out.release()
cv2.destroyAllWindows()
