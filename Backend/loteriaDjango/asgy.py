"""
ASGI config for loteriaDjango project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loteriaDjango.settings')

# Para solo HTTP (sin WebSockets aún):
application = get_asgi_application()

# Para WebSockets (cuando instales Channels):
"""
from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": ... (aquí irían tus WebSockets)
})
"""