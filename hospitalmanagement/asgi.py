import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import hospital.routing  # your app where websocket_urlpatterns is defined

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospitalmanagement.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            hospital.routing.websocket_urlpatterns
        )
    ),
})
