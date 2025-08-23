from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='base_para_informes'),
]