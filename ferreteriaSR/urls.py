from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('productos/', include('productos.urls')),
    #path('proveedores/', include('proveedores.urls')),
    #path('pedidos/', include('pedidos.urls')),
    #path('ventas/', include('ventas.urls')),
    #path('informes/', include('informes.urls')),
]
