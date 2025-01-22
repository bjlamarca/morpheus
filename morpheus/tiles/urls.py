from django.urls import path
from . import views

app_name = "tiles"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("create/", views.page_create_view, name="create"),
    path("detail/<int:page_id>", views.page_detail_view, name="detail"),
    path("page-list/", views.PageListView.as_view(), name="page-list"),
    
    
    
    path("scene-tile/", views.scene_tile_view, name="scene-tile"),
    path("nav-tile/", views.nav_tile_view, name="nav-tile"),
    path("page/", views.tile_page_view, name="page-tile"),
    path("home/", views.tiles_main_view, name="main"),



]