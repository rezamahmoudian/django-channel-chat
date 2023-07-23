import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_django_channel.settings")
django_asgi_app = get_asgi_application()

import chat.routing

# dadan proje be dast asgi
# tarif protocol baraye shabake va vazife masiryabi beyn anhara b ProtocolTypeRouter
# masir yabi bar asas noe protocol
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
        # Just HTTP for now. (We can add other protocols later.)
    }
)
