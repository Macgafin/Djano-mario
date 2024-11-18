import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from mario.routing import websocket_urlpatterns  # type: ignore # routing.pyのパスをインポート

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
