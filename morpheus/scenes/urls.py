from django.urls import path

from . import views

app_name = "scenes"

urlpatterns = [
    path('', views.scene_main_view, name='main'),
    path('scene-list/', views.SceneListView.as_view(), name='scene-list'),
    path('create/', views.scene_create_view, name='create'),
    path('detail/<int:scene_id>', views.scene_detail_view, name='detail'),
    path('scene-add-device/<int:scene_id>', views.scene_add_device_view, name='add-device'),
    path('scene-add-device-list/<int:scene_id>', views.scene_add_device_list_view, name='add-device-list'),
    path('scene-device-list/<int:scene_id>', views.scene_device_list_view, name='device-list'),
    path('scene-device-list-area/<int:scene_id>', views.scene_device_list_area_view, name='device-list-area'),
    path('scene-adjust/', views.scene_adjust_view, name='scene-adjust'),
    
    ]