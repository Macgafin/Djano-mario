from django.urls import path
from .consumers import GameInfoConsumer


websocket_urlpatterns = [
    path('ws/game-info/', GameInfoConsumer.as_asgi()),  # WebSocketのURLを指定
]
