import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

from django.core.asgi import get_asgi_application

# Initialize Django first
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack

from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)

from channels.security.websocket import (
    AllowedHostsOriginValidator,
)

from websocket.routing import websocket_urlpatterns


application = ProtocolTypeRouter({

    # Normal HTTP requests
    "http": django_asgi_app,

    # WebSocket requests
    "websocket": AllowedHostsOriginValidator(

        AuthMiddlewareStack(

            URLRouter(
                websocket_urlpatterns
            )

        )

    ),

})