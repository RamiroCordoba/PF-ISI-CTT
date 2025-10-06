from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('productos/', include('productos.urls')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('ventas/', include('ventas.urls')),
    path('informes/', include('reporte.urls')),
    #path('proveedores/', include('proveedores.urls')),
    #path('pedidos/', include('pedidos.urls')),
    #path('ventas/', include('ventas.urls')),
    #path('informes/', include('informes.urls')),
]

handler400 = 'dashboard.views.custom_400_view'
handler403 = 'dashboard.views.custom_403_view'
handler404 = 'dashboard.views.custom_404_view'
handler500 = 'dashboard.views.custom_500_view'
# NOTA: Django solo soporta handlers automáticos para 400, 403, 404 y 500.
# Otros errores (401, 408, 429, 502, 503, 504) requieren manejo manual en views o middleware.
