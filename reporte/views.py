# API para obtener vendedores
from usuarios.models import UsuarioPersonalizado
from django.contrib.auth.models import Group

def vendedores_api(request):
    try:
        vendedor_group = Group.objects.get(name='Vendedor')
    except Group.DoesNotExist:
        return JsonResponse({'vendedores': []})
    vendedores = UsuarioPersonalizado.objects.filter(groups=vendedor_group, is_active=True).order_by('first_name', 'last_name')
    data = [{'id': v.id, 'nombre': f"{v.first_name} {v.last_name}".strip() or v.email} for v in vendedores]
    return JsonResponse({'vendedores': data})
from productos.models import Categoria
from django.http import JsonResponse
from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'reportes/index_report.html')

def rep_ventas_generales_view(request):
    # Obtener parámetros GET
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    vendedores = request.GET.getlist('vendedores')
    categorias = request.GET.getlist('categorias')
    context = {
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'vendedores': vendedores,
        'categorias': categorias,
    }
    return render(request, 'reportes/rep_ventas_generales.html', context)

# API para obtener categorías de productos
def categorias_api(request):
    categorias = Categoria.objects.all().order_by('nombre')
    data = [{'id': c.id, 'nombre': c.nombre} for c in categorias]
    return JsonResponse({'categorias': data})