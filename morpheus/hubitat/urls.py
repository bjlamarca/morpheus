from django.urls import path
from . import views

app_name = "hubitat"

urlpatterns = [

    path('receive/', views.hubitat_receive_view, name='receive'),
]