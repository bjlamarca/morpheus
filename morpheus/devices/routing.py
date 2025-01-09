from django.urls import re_path, path

from . import consumers

devices_websocket_urlpatterns = [
    re_path(r"ws/devices/gen/$", consumers.GenConsumer.as_asgi()),
    
]