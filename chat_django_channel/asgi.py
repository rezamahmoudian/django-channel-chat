import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_django_channel.settings")


# dadan proje be dast asgi
# tarif protocol baraye shabake va vazife masiryabi beyn anhara b ProtocolTypeRouter
# masir yabi bar asas noe protocol
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns)
        )),
        # Just HTTP for now. (We can add other protocols later.)
    }
)
