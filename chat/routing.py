# we use re_path due to the limitations that we have in url router
from django.urls import re_path

from . import consumers

websocket_urlpatters = [
    # route for ChatConsumer
    # in the path method, we are going to set this endpoint as what we specified
    # in the front end whenever we try to make that initial socket connection
    re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
]