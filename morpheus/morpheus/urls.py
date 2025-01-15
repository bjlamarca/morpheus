from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('hue/', include('hue.urls')),
    path('devices/', include('devices.urls')),
    path('scenes/', include('scenes.urls')),
    path('navbar/', views.navbar_view, name="navbar"),
    path('admin/', admin.site.urls),
]
