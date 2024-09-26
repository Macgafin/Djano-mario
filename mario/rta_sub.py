import cv2
from pathlib import Path

def video_stream():
    # OBSの仮想カメラから映像をキャプチャ
    cap = cv2.VideoCapture(2)  # 仮想カメラのIDが2と仮定

    if not cap.isOpened():
        print("Error: カメラが開けませんでした")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            print("Error: フレームをキャプチャできませんでした")
            break

    cap.release()
