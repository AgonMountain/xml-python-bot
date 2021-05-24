from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('config/', views.ConfigView.as_view(), name='config'),
    path('schemes/', views.SchemesView.as_view(), name='schemes'),
    path('schemes/<int:pk>/update', views.SchemeUpdateView.as_view(), name='scheme-update'),
    path('schemes/<int:pk>/delete', views.SchemeDeleteView.as_view(), name='scheme-delete'),
    path('elements/<int:pk>/update', views.ElementUpdateView.as_view(), name='element-update'),
    path('elements/<int:pk>/delete', views.ElementDeleteView.as_view(), name='element-delete'),
    path('additions/<int:pk>/update', views.ElementAdditionUpdateView.as_view(),
         name='addition-update'),
    path('additions/<int:pk>/delete', views.ElementAdditionDeleteView.as_view(),
         name='addition-delete'),
    path('transitions/<int:pk>/update', views.ElementTransitionUpdateView.as_view(),
         name='transition-update'),
    path('transitions/<int:pk>/delete', views.ElementTransitionDeleteView.as_view(),
         name='transition-delete'),

]
