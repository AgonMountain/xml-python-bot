from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('config', views.config),
    path('users', views.users),
    path('schemes', views.schemes),
]
