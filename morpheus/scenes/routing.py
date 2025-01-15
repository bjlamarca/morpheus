from django.urls import re_path, path

from . import consumers

scenes_websocket_urlpatterns = [
    re_path(r"ws/scenes/scene/$", consumers.SceneConsumer.as_asgi()),
    
]