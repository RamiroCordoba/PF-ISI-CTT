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
    path('articulos/<int:pk>/proveedores/', proveedores_grilla, name='proveedores_grilla'),
    path('articulos/<int:pk>/proveedores/quitar/<int:proveedor_id>/', quitar_proveedor, name='quitar_proveedor'),

    #__ Carga masiva
    path('articulos/carga_masiva_productos/', CargaMasivaProductosView.as_view(), name='carga_masiva_productos'),
    path('articulos/exportar_productos/', ExportarProductosExcelView.as_view(), name='exportar_productos'),

    #__________ Proveedor
    path('Proveedor/', ProveedorList.as_view(), name='mis_proveedores'),
    path('Proveedor/nuevo_proveedor/', ProveedorCreate.as_view(), name='nuevo_proveedor'),
    path('Proveedor/editar_proveedor/<int:pk>/', ProveedorUpdate.as_view(), name='editar_proveedor'),
    path('Proveedor/eliminar_proveedor/<int:pk>/', ProveedorDelete.as_view(), name='eliminar_proveedor'),
    path('Proveedor/informacion/<int:pk>/', ProveedorDetail.as_view(), name='detalles_de_proveedor'),

        #__________ Estacionalidad
    path('Estacionalidad/', EstacionalidadList.as_view(), name='mis_estacionalidades'),
    path('Estacionalidad/nueva_estacionalidad/', EstacionalidadCreate.as_view(), name='nueva_estacionalidad'),
    path('Estacionalidad/editar_estacionalidad/<int:pk>/', EstacionalidadUpdate.as_view(), name='editar_estacionalidad'),
    path('Estacionalidad/eliminar_estacionalidad/<int:pk>/', EstacionalidadDelete.as_view(), name='eliminar_estacionalidad'),
    path('Estacionalidad/informacion/<int:pk>/', EstacionalidadDetail.as_view(), name='detalles_de_estacionalidad'),
    #__________ Pedidos
    path('pedidos/', PedidosList.as_view(), name='listar_pedidos'),
    path('pedidos/nuevo/', PedidoCreateView.as_view(), name='nuevo_pedido'),
    path('autocomplete_productos/', autocomplete_productos, name='autocomplete_productos'),
    path('ajax/productos_por_proveedor/', productos_por_proveedor, name='productos_por_proveedor'),
    path('pedidos/editar_pedidos/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('pedidos/informacion/<int:pk>/', PedidoDetailView.as_view(), name='detalle_de_pedido'),
    path('pedidos/eliminar_pedido/<int:pk>/', PedidoDelete.as_view(), name='eliminar_pedido'),
]