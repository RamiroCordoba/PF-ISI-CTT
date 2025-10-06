from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Sum
from productos.models import PedidoItem, Producto
from django.db import models
from ventas.models import Venta
from django.utils import timezone

@login_required
def dashboard_view(request):
    from productos.models import Producto, Pedido, Proveedor
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()
    total_proveedores = Proveedor.objects.count()

    hoy = timezone.now().date()
    ventas_mes_actual = Venta.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month,
        completado=True,
        anulada=False
    ).count()

    # Nombre del mes actual en español
    import calendar
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    mes_actual_nombre = meses[hoy.month - 1]

    es_vendedor = request.user.groups.filter(name='vendedor').exists()
    return render(request, 'dashboard/principal.html', {
        'total_productos': total_productos,
        'total_pedidos': total_pedidos,
        'total_proveedores': total_proveedores,
        'ventas_mes_actual': ventas_mes_actual,
        'mes_actual_nombre': mes_actual_nombre,
        'es_vendedor': es_vendedor
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

def custom_404_view(request, exception):
    return render(request, 'errores/404.html', status=404)

def custom_403_view(request, exception=None):
    return render(request, 'errores/403.html', status=403)

def custom_400_view(request, exception):
    return render(request, 'errores/400.html', status=400)

def custom_500_view(request):
    return render(request, 'errores/500.html', status=500)

def custom_401_view(request, exception=None):
    return render(request, 'errores/401.html', status=401)

def custom_408_view(request, exception=None):
    return render(request, 'errores/408.html', status=408)

def custom_429_view(request, exception=None):
    return render(request, 'errores/429.html', status=429)

def custom_502_view(request, exception=None):
    return render(request, 'errores/502.html', status=502)

def custom_503_view(request, exception=None):
    return render(request, 'errores/503.html', status=503)

def custom_504_view(request, exception=None):
    return render(request, 'errores/504.html', status=504)
