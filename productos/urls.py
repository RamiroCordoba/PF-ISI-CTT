from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    path('categorias/', CategoriaList.as_view(), name='categorias'),
    path('categorias/nueva_categoria/', CategoriaCreate.as_view(), name='nueva_categoria'),
    path('categorias/editar_categoria/<int:pk>/', CategoriaUpdate.as_view(), name='editar_categoria'),
    path('categorias/eliminar_categoria/<int:pk>/', CategoriaDelete.as_view(), name='eliminar_categoria'),
]