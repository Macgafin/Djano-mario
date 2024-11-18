import asyncio
import json
from pathlib import Path
import time
import aiofiles
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

from django.conf import settings
from .viewservices import process_game_info

logger = logging.getLogger(__name__)

class GameInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # WebSocket接続が開始された時の処理
        self.group_name = 'game_info'
        
        # グループに参加
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"Connected to {self.group_name} group")
    
    async def disconnect(self, close_code):
        # WebSocket接続が切断された時の処理
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"Disconnected from {self.group_name} group")
        
    

    async def receive(self, text_data):
        
        # text_empty = json.loads(text_data)
        
        # message = text_empty['message']
        
        # WebSocketからデータを受け取った時の処理
        logger.info(f"Received data from WebSocket: {text_data}")
        
        # ゲーム情報
        game_info = []
        
        # 読み込むテキストファイルのパスを設定
        text_file_path = Path(settings.BASE_DIR) / 'mario' / 'static' / 'mario' / 'realtime_analytics.txt'
        
        # 設定からコードとテキストのマッピングを取得
        code_texts = settings.CODE_TEXTS
        
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

            # `process_game_info`を呼び出して`collision_message`を取得
        try:
            current_time = time.time()
            collision_message = await asyncio.to_thread(process_game_info, game_info, current_time)
        except Exception as e:
            logger.error(f"Error in process_game_info: {e}")
            collision_message = []
        
        await self.send(text_data=json.dumps({
            # 'response': f'Received your message: {text_data}'
            "response" : game_info,
            "collision_message" : collision_message
        }))
       
    
    # 'group_send'によって呼び出されるメソッド
    async def send_game_info(self, event):
        print("send_game_info called")  # ここを追加
        game_info = event['message']
        print(f"send_game_info called with: {game_info}")  # 追加のデバッグ出力
        
        # WebSocketにメッセージを送信
        await self.send(text_data=json.dumps({
            'game_info': game_info
        }))
        logger.info(f"Sending game info: {game_info}")
        
    
    #""によってスクリプトを送るメソッド
    async def send_collision_message(self, event):
        print("collision message called")  # ここを追加
        collision_message = event['message']
        print(f"send_game_info called with: {collision_message}")  # 追加のデバッグ出力
        
        # WebSocketにメッセージを送信
        await self.send(text_data=json.dumps({
            'collision_message': collision_message
        }))
        logger.info(f"Sending game info: {collision_message}")
    