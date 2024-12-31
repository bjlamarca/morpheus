from django.urls import path

from . import views

app_name = "hue"

urlpatterns = [
    path("", views.hue_main_view, name="main"),
    path("tools/", views.tools_view, name="tools"),
    path("device-list/", views.DeviceListView.as_view(), name="device-list"),
    path("light-list/", views.LightListView.as_view(), name="light-list")
]