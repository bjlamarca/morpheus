from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('hue/', include('hue.urls')),
    path('admin/', admin.site.urls),
]
