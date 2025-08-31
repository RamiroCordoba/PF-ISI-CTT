from django.urls import path, include
from .views import *

urlpatterns = [
    path("select2/", include("django_select2.urls")), 

    #Iva
    path('iva/', IvaList.as_view(), name='mis_iva'),
    path('iva/nuevo_iva/', IvaCreate.as_view(), name='nuevo_iva'),
    path('iva/editar_iva/<int:pk>/', IvaUpdate.as_view(), name='editar_iva'),
    path('iva/informacion/<int:pk>/', IvaDetail.as_view(), name='detalles_iva'),
    path('iva/eliminar_iva/<int:pk>/', IvaDelete.as_view(), name='eliminar_iva'),
    #Moneda
    path('moneda/', MonedaList.as_view(), name='mis_monedas'),
    path('moneda/nueva_moneda/', MonedaCreate.as_view(), name='nueva_moneda'),
    path('moneda/editar_moneda/<int:pk>/', MonedaUpdate.as_view(), name='editar_moneda'),
    path('moneda/informacion/<int:pk>/', MonedaDetail.as_view(), name='detalles_moneda'),
    path('moneda/eliminar_moneda/<int:pk>/', MonedaDelete.as_view(), name='eliminar_moneda'),   
    #Condicion Fiscal
    path('condicion_fiscal/', CondicionFiscalList.as_view(), name='mis_condiciones_fiscales'),
    path('condicion_fiscal/nueva_condicion_fiscal/', CondicionFiscalCreate.as_view(), name='nueva_condicion_fiscal'),
    path('condicion_fiscal/editar_condicion_fiscal/<int:pk>/', CondicionFiscalUpdate.as_view(), name='editar_condicion_fiscal'),
    path('condicion_fiscal/informacion/<int:pk>/', CondicionFiscalDetail.as_view(), name='detalles_condicion_fiscal'),
    path('condicion_fiscal/eliminar_condicion_fiscal/<int:pk>/', CondicionFiscalDelete.as_view(), name='eliminar_condicion_fiscal'),
    #Cliente
    path('cliente/', ClienteList.as_view(), name='mis_clientes'),
    path('cliente/nuevo_cliente/', ClienteCreate.as_view(), name='nuevo_cliente'),
    path('cliente/editar_cliente/<int:pk>/', ClienteUpdate.as_view(), name='editar_cliente'),
    path('cliente/informacion/<int:pk>/', ClienteDetail.as_view(), name='detalles_cliente'),
    path('cliente/eliminar_cliente/<int:pk>/', ClienteDelete.as_view(), name='eliminar_cliente'),
    #Venta
    path('venta/', VentaList.as_view(), name='mis_ventas'),
    path('venta/nueva_venta/', VentaCreate.as_view(), name='nueva_venta'),
    path('venta/editar_venta/<int:pk>/', VentaUpdate.as_view(), name='editar_venta'),
    path('venta/informacion/<int:pk>/', VentaDetail.as_view(), name='detalles_venta'),
    path('venta/eliminar_venta/<int:pk>/', VentaDelete.as_view(), name='eliminar_venta'),
    path('venta/<int:pk>/pdf/', venta_pdf_view, name='venta_pdf'),
    path('ajax/obtener_precio/', obtener_precio, name='obtener_precio_producto'),
    path('ajax/buscar_productos2/', buscar_productos2, name='buscar_productos2'),
    path('autocomplete-productos2/', autocomplete_productos2, name='autocomplete_productos2'),
    path('autocomplete-clientes/', autocomplete_clientes, name='autocomplete_clientes'),
    # Notas de crédito
    path('notacredito/', NotaCreditoList.as_view(), name='mis_notascredito'),
    path('notacredito/<int:pk>/', NotaCreditoDetail.as_view(), name='detalles_notacredito'),
    path('autocomplete/formas-pago/', autocomplete_formas_pago, name='autocomplete_formas_pago'),

]