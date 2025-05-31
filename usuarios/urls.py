from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
app_name = 'usuarios'
urlpatterns = [
    path('', views.UsuarioListView.as_view(), name='listar_usuarios'),
    path('nuevo_usuario/', views.UsuarioCreateView.as_view(), name='nuevo_usuario'),
    path('editar_usuario/<int:pk>/', views.UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('eliminar_usuario/<int:pk>/', views.UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('detalle_usuario/<int:pk>/', views.UsuarioDetailView.as_view(), name='detalle_usuario'),

]
