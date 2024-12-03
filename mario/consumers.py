import asyncio
import json
from pathlib import Path
import time
import aiofiles
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
from django.conf import settings
from .viewservices import (
    process_game_info,
)  # views.py の process_game_info をインポート

logger = logging.getLogger(__name__)


class GameInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # WebSocket接続が開始された時の処理
        self.group_name = "game_info"

        # グループに参加
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        logger.info(f"Connected to {self.group_name} group")

    async def disconnect(self, close_code):
        # WebSocket接続が切断された時の処理
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"Disconnected from {self.group_name} group")

    async def receive(self, text_data):
        collision_message = ""

        # ゲーム情報の取得
        game_info = await self.get_game_info()

        # ゲーム情報とフィードバックメッセージを process_game_info に渡して処理する
        current_time = time.time()  # 現在の時刻を取得
        try:
            collision_message = await asyncio.to_thread(
                process_game_info, game_info, current_time
            )
        except Exception as e:
            logger.error(f"Error in process_game_info: {e}")

        # フィードバックが「巻き戻し中！」や「問題なし」でない場合にファイルに書き込む
        if collision_message and collision_message not in ["巻き戻し中！", "問題なし"]:
            await self.write_feedback_to_file(collision_message)


        # feedback.txt からフィードバックメッセージを非同期で読み込む
        collision_message = await self.read_feedback_file()


        # 読み込んだフィードバックメッセージとゲーム情報を WebSocket 経由で送信
        await self.send_game_info_to_websocket(game_info, collision_message)

    # feedback.txt を非同期で読み込む
    async def read_feedback_file(self):
        feedback_file_path = (
            Path(settings.BASE_DIR) / "mario" / "static" / "mario" / "feedback.txt"
        )

        try:
            if feedback_file_path.exists():
                async with aiofiles.open(
                    feedback_file_path, "r", encoding="utf-8"
                ) as file:
                    # ファイル全体を読み込む
                    content = await file.read()
                    if content:
                        return content.strip()  # 内容があればそのまま返す
        except Exception as e:
            logger.error(f"Error reading feedback file: {e}")
            return "フィードバック読み込みエラー"

    # ゲーム情報を非同期で取得
    async def get_game_info(self):
        game_info = []
        text_file_path = (
            Path(settings.BASE_DIR)
            / "mario"
            / "static"
            / "mario"
            / "realtime_analytics.txt"
        )
        code_texts = settings.CODE_TEXTS

        try:
            if text_file_path.exists():
                async with aiofiles.open(text_file_path, "r") as file:
                    async for line in file:
                        data = line.strip().split()
                        if len(data) >= 6 and data[0] in code_texts:
                            game_info.append(
                                {
                                    "code": code_texts[data[0]],
                                    "x": float(data[1]),
                                    "y": float(data[2]),
                                    "width": float(data[3]),
                                    "height": float(data[4]),
                                    "confidence": float(data[5]),
                                    "timestamp": float(data[6]),
                                }
                            )
            else:
                game_info.append({"error": "ファイルが見つかりません。"})
        except Exception as e:
            logger.exception("Error reading the game info file.")
            game_info.append(
                {"error": "ゲーム情報の読み込み中にエラーが発生しました。"}
            )

        return game_info

    # WebSocket経由でゲーム情報とフィードバックメッセージ（collision_message）を送信
    async def send_game_info_to_websocket(self, game_info, collision_message):
        await self.send(
            text_data=json.dumps(
                {
                    "response": game_info,  # ゲーム情報
                    "collision_message": collision_message,  # フィードバックメッセージ（collision_message）
                }
            )
        )

    # feedback.txt にフィードバックメッセージを書き込む
    async def write_feedback_to_file(self, feedback_message):
        feedback_file_path = (
            Path(settings.BASE_DIR) / "mario" / "static" / "mario" / "feedback.txt"
        )
        try:
            async with aiofiles.open(feedback_file_path, "w", encoding="utf-8") as file:
                await file.write(f"{feedback_message}\n")
            logger.info("Feedback written to feedback.txt")
        except Exception as e:
            logger.error(f"Error writing to feedback.txt: {e}")

    # 'group_send' によって呼び出されるメソッド
    async def send_game_info(self, event):
        # ここではゲーム情報を送信する処理
        game_info = event["message"]
        await self.send(text_data=json.dumps({"game_info": game_info}))
        logger.info(f"Sending game info: {game_info}")

    # 'group_send' によって呼び出されるメソッド
    async def send_collision_message(self, event):
        # ここでは衝突メッセージを送信する処理
        collision_message = event["message"]
        await self.send(text_data=json.dumps({"collision_message": collision_message}))
        logger.info(f"Sending collision message: {collision_message}")
