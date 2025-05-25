from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    #__________ Categorias
    path('categorias/', CategoriaList.as_view(), name='categorias'),
    path('categorias/nueva_categoria/', CategoriaCreate.as_view(), name='nueva_categoria'),
    path('categorias/editar_categoria/<int:pk>/', CategoriaUpdate.as_view(), name='editar_categoria'),
    path('categorias/eliminar_categoria/<int:pk>/', CategoriaDelete.as_view(), name='eliminar_categoria'),
    #__________ Productos
    path('productos/misproductos', ProductoList.as_view(), name='misproductos'),
    path('productos/nuevo_producto/', ProductoCreate.as_view(), name='nuevo_producto'),
    path('productos/editar_producto/<int:pk>/', ProductoUpdate.as_view(), name='editar_producto'),
    path('productos/eliminar_producto/<int:pk>/', ProductoDelete.as_view(), name='eliminar_producto'),
]