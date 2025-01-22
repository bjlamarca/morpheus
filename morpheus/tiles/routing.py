from django.urls import re_path, path

from . import consumers

tiles_websocket_urlpatterns = [
    re_path(r"ws/tiles/ui/$", consumers.TileUIConsumer.as_asgi()),
    re_path(r"ws/tiles/gen/$", consumers.TileConsumer.as_asgi()),
    
]