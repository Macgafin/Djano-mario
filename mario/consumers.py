import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, game_info):
        text_data_json = json.loads(game_info)
        game_info = text_data_json['game_info']

        # 受信したデータをクライアントに送信
        await self.send(text_data=json.dumps({
            'message': "ahow"
        }))
