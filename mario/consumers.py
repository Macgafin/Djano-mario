import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

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
        # WebSocketからデータを受け取った時の処理
        logger.info(f"Received data from WebSocket: {text_data}")
    
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
