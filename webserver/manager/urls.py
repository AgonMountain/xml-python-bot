from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('config', views.bot_config),
    # path('users', views.bot_users),
    # path('schemes', views.bot_schemes),
    #
    # path('scheme', views.scheme),
    # path('element', views.element),
    # path('addition', views.addition),
    # path('transition', views.transition),

]
