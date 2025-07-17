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
    path('articulos/', ArticuloList.as_view(), name='mis_articulos'),
    path('articulos/nuevo_articulo/', ArticuloCreate.as_view(), name='nuevo_articulo'),
    path('articulos/editar_articulo/<int:pk>/', ArticuloUpdate.as_view(), name='editar_articulo'),
    path('articulos/eliminar_articulo/<int:pk>/', ArticuloDelete.as_view(), name='eliminar_articulo'),
    path('articulos/informacion/<int:pk>/', ArticuloDetail.as_view(), name='detalles_de_articulo'),
    #__________ Proveedor
    path('Proveedor/', ProveedorList.as_view(), name='mis_proveedores'),
    path('Proveedor/nuevo_proveedor/', ProveedorCreate.as_view(), name='nuevo_proveedor'),
    path('Proveedor/editar_proveedor/<int:pk>/', ProveedorUpdate.as_view(), name='editar_proveedor'),
    path('Proveedor/eliminar_proveedor/<int:pk>/', ProveedorDelete.as_view(), name='eliminar_proveedor'),
    path('Proveedor/informacion/<int:pk>/', ProveedorDetail.as_view(), name='detalles_de_proveedor')
]