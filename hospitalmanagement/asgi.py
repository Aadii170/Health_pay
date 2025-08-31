import os

# ⬅️ settings must be configured first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalmanagement.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# ⬅️ only import your apps after settings are loaded
import hospital.routing
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            hospital.routing.websocket_urlpatterns +
            chat.routing.websocket_urlpatterns
        )
    ),
})
