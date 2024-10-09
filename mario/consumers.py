import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"WebSocket connection attempt from {self.channel_name}")  # 追加
        await self.channel_layer.group_add(
            'game_info',  # ここはviews.pyで指定したグループ名と一致させます
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connection established for {self.channel_name}")  # 追加

    async def disconnect(self, _): #アンダースコアとして後半の引数は使わないものとする
        await self.channel_layer.group_discard(
            'game_info',
            self.channel_name
        )

    async def send_game_info(self, event):
        message = event['message']

        # WebSocketを通じてクライアントにメッセージを送信
        await self.send(text_data=json.dumps(message))
