from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('config', views.bot_config, name='config'),
    path('users', views.bot_users, name='users'),
    path('schemes', views.bot_schemes, name='schemes'),

    path('scheme', views.scheme, name='scheme'),
    path('element', views.element, name='element'),
    path('addition', views.addition, name='addition'),
    path('transition', views.transition, name='transition'),

]
