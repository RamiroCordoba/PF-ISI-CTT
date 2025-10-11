from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'usuarios'
urlpatterns = [
    path('cambiar_contrasena_ajax/', views.CambiarContrasenaAjaxView.as_view(), name='cambiar_contrasena_ajax'),
    path('', views.UsuarioListView.as_view(), name='listar_usuarios'),
    path('nuevo_usuario/', views.UsuarioCreateView.as_view(), name='nuevo_usuario'),
    path('editar_usuario/<int:pk>/', views.UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('eliminar_usuario/<int:pk>/', views.UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('detalle_usuario/<int:pk>/', views.UsuarioDetailView.as_view(), name='detalle_usuario'),
    path('mi_perfil/', views.UsuarioPerfilView.as_view(), name='mi_perfil'),
    path('cambiar_contrasena/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/password_change_form.html',
        success_url='/usuarios/cambiar_contrasena/hecho/'
    ), name='cambiar_contrasena'),
        path('editar_perfil_modal/<int:pk>/', views.PerfilModalUpdateView.as_view(), name='editar_perfil_modal'),
    path('cambiar_contrasena/hecho/', auth_views.PasswordChangeDoneView.as_view(template_name='usuarios/password_change_done.html'), name='password_change_done'),
]

