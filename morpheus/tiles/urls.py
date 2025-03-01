from django.urls import path
from . import views

app_name = "tiles"

urlpatterns = [
    path("", views.tiles_main_view, name="home"),
    
       
    
    
    path("scene-tile/", views.tiles_scene_view, name="scene-tile"),
    path("nav-tile/", views.tiles_nav_view, name="nav-tile"),
    path("page/", views.tiles_page_view, name="page-tile"),
    path("home/", views.tiles_main_view, name="main"),

    path("admin/", views.admin_view, name="admin"),
    path("admin/page", views.page_main_view, name="page-main"),
    path("admin/create/", views.page_create_view, name="create"),
    path("admin/detail/<int:page_id>", views.page_detail_view, name="detail"),
    path("admin/page-list/", views.PageListView.as_view(), name="page-list"),
    path("admin/section-list/<int:page_id>", views.section_list_view, name="section-list"),
    path("admin/section-create/<int:page_id>" , views.section_create_view, name="section-create"),
    path("admin/section-detail/<int:section_id>", views.section_detail_view, name="section-detail"),
    path("admin/tiles-list/<int:section_id>", views.tiles_list_view, name="tiles-list"),



]