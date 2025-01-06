from django.urls import re_path, path

from . import consumers

hue_websocket_urlpatterns = [
    re_path(r"ws/hue/diag/$", consumers.DiagConsumer.as_asgi()),
    re_path(r"ws/hue/gen/$", consumers.GenConsumer.as_asgi()),
]