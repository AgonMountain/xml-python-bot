from django.urls import path
from . import views

urlpatterns = [
    path('manager', views.main),
    path('login', views.login),
]
