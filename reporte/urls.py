from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='base_para_informes'),
    path('reportes/rep_ventas_generales', views.rep_ventas_generales_view, name='rep_ventas_generales'),
    path('reportes/categorias_api', views.categorias_api, name='categorias_api'),
    path('reportes/vendedores_api', views.vendedores_api, name='vendedores_api'),
]
