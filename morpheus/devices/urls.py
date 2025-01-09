from django.urls import path
from . import views

app_name = "devices"

urlpatterns = [
    path('', views.devices_main_view, name='main'),
    path('device-list/', views.DeviceListView.as_view(), name='device-list'),
    path('device-detail/<int:device_id>', views.device_detail_view, name='device-detail')
]