"""
ASGI config for mywebsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import chat.routing

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    # o	Use the AuthMiddlewareStack to wrap the url router
    'websocket':AuthMiddlewareStack(
        #In the URLRouter we’ll just pass in the websocket url patters list from
        # our routing.py file
        URLRouter(
            chat.routing.websocket_urlpatters
        )
    )
})
