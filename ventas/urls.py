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
    path('condicion_fiscal/', CondicionFiscalList.as_view(), name='mis_condiciones_ficales'),
    path('condicion_fiscal/nueva_condicion_fiscal/', CondicionFiscalCreate.as_view(), name='nueva_condicion_fiscal'),
    path('condicion_fiscal/editar_condicion_fiscal/<int:pk>/', CondicionFiscalUpdate.as_view(), name='editar_condicion_fiscal'),
    path('condicion_fiscal/informacion/<int:pk>/', CondicionFiscalDetail.as_view(), name='detalles_condicion_fiscal'),
    path('condicion_fiscal/eliminar_condicion_fiscal/<int:pk>/', CondicionFiscalDelete.as_view(), name='eliminar_condicion_fiscal'),    
]