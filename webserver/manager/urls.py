from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('config', views.ConfigView.as_view(), name='config'),
    path('users', views.UsersView.as_view(), name='users'),
    path('schemes', views.bot_schemes, name='schemes'),

    path('scheme', views.scheme, name='scheme'),
    path('element', views.element, name='element'),
    path('addition', views.addition, name='addition'),
    path('transition', views.transition, name='transition'),

]
