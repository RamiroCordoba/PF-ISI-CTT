from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('top-10-productos/',views.top_10_productos_mas_pedidos,name='top_10_productos_mas_pedidos'),

]
