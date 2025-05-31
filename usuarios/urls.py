from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
app_name = 'usuarios'
urlpatterns = [
    path('', views.UsuarioListView.as_view(), name='listar_usuarios'),
    path('nuevo_usuario/', views.UsuarioCreateView.as_view(), name='nuevo_usuario'),
]
