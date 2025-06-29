from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    # Recuperación de contraseña
    path(
    'password_reset/',
    auth_views.PasswordResetView.as_view(
        template_name='restablecedor/password_reset_form.html',
        email_template_name='restablecedor/password_reset_email.txt',         # versión texto plano por si tiene bloqueado HTML el usuario
        html_email_template_name='restablecedor/password_reset_email.html',   # <- versión moderna con HTML
        subject_template_name='restablecedor/password_reset_subject.txt'
    ),
    name='password_reset'
),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='restablecedor/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='restablecedor/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='restablecedor/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
