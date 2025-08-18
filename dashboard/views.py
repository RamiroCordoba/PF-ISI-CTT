from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Sum
from productos.models import PedidoItem, Producto
from django.db import models

@login_required
def dashboard_view(request):
    from productos.models import Producto, Pedido, Proveedor
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()
    total_proveedores = Proveedor.objects.count()
    return render(request, 'dashboard/principal.html', {
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
        'total_proveedores': total_proveedores
    })


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def top_10_productos_mas_pedidos(request):
    datos = (
        PedidoItem.objects
        .values('producto__nombre')
        .annotate(total=Sum('cantidad'))
        .order_by('-total')[:10]
    )
    labels = [item['producto__nombre'] or 'Sin nombre' for item in datos]
    data = [item['total'] for item in datos]
    return JsonResponse({'labels': labels, 'data': data})

@login_required
def productos_stock_minimo(request):
    productos = Producto.objects.filter(stock__lt=models.F('stock_minimo'))
    resultado = [
        {
            'nombre': p.nombre,
            'stock_actual': p.stock,
            'stock_minimo': p.stock_minimo if p.stock_minimo is not None else 0
        }
        for p in productos
    ]
    return JsonResponse(resultado, safe=False)
