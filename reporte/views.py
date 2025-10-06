from usuarios.models import UsuarioPersonalizado
from django.contrib.auth.models import Group
from productos.models import Categoria
from django.http import JsonResponse
from usuarios.models import UsuarioPersonalizado
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from productos.models import Categoria
from django.http import JsonResponse
from django.shortcuts import render
import logging

def vendedores_api(request):
    try:
        vendedor_group = Group.objects.get(name='Vendedor')
    except Group.DoesNotExist:
        return JsonResponse({'vendedores': []})
    vendedores = UsuarioPersonalizado.objects.filter(groups=vendedor_group, is_active=True).order_by('first_name', 'last_name')
    data = [{'id': v.id, 'nombre': f"{v.first_name} {v.last_name}".strip() or v.email} for v in vendedores]
    return JsonResponse({'vendedores': data})


def vendedores_api(request):
    try:
        vendedor_group = Group.objects.get(name='Vendedor')
    except Group.DoesNotExist:
        return JsonResponse({'vendedores': []})
    vendedores = UsuarioPersonalizado.objects.filter(groups=vendedor_group, is_active=True).order_by('first_name', 'last_name')
    data = [{'id': v.id, 'nombre': f"{v.first_name} {v.last_name}".strip() or v.email} for v in vendedores]
    return JsonResponse({'vendedores': data})


logger = logging.getLogger(__name__)


@login_required
def dashboard_view(request):
    es_vendedor = request.user.groups.filter(name__iexact='vendedor').exists()
    if es_vendedor and not (request.user.is_superuser or request.user.is_staff):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()
    return render(request, 'reportes/index_report.html')

@login_required
def rep_ventas_generales_view(request):
    es_vendedor = request.user.groups.filter(name__iexact='vendedor').exists()
    if es_vendedor and not (request.user.is_superuser or request.user.is_staff):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()
    # Obtener parámetros GET
    from datetime import datetime
    fecha_desde_str = request.GET.get('fecha_desde', '')
    fecha_hasta_str = request.GET.get('fecha_hasta', '')
    fecha_desde = None
    fecha_hasta = None
    if fecha_desde_str:
        try:
            fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date()
        except Exception:
            fecha_desde = None
    if fecha_hasta_str:
        try:
            fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date()
        except Exception:
            fecha_hasta = None
    vendedores_seleccionados = request.GET.getlist('vendedores')
    categorias_seleccionadas = request.GET.getlist('categorias')

    # Obtener todos los vendedores (solo los con rol Vendedor y activos)
    try:
        vendedor_group = Group.objects.get(name='Vendedor')
        vendedores_qs = UsuarioPersonalizado.objects.filter(groups=vendedor_group, is_active=True).order_by('first_name', 'last_name')
    except Group.DoesNotExist:
        vendedores_qs = UsuarioPersonalizado.objects.none()
    vendedores = [{'id': str(v.id), 'nombre': f"{v.first_name} {v.last_name}".strip() or v.email} for v in vendedores_qs]

    # Obtener todas las categorías
    categorias_qs = Categoria.objects.all().order_by('nombre')
    categorias = [{'id': str(c.id), 'nombre': c.nombre} for c in categorias_qs]

    # --- FILTROS ---
    from ventas.models import Venta, VentaItem, NotaCredito, NotaCreditoItem
    from productos.models import Producto
    from django.db.models import Sum, Count, Q
    import datetime
    ventas_qs = Venta.objects.all()
    if fecha_desde:
        ventas_qs = ventas_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        ventas_qs = ventas_qs.filter(fecha__lte=fecha_hasta)
    # Filtrado vendedores
    if vendedores_seleccionados and 'todos' not in vendedores_seleccionados:
        # El campo vendedor en Venta es un string (nombre), no un ID
        vendedores_nombres = [v for v in vendedores_seleccionados if v != 'todos']
        ventas_qs = ventas_qs.filter(vendedor__in=vendedores_nombres)

    # Filtrado categorías
    if categorias_seleccionadas and 'todas' not in categorias_seleccionadas:
        categorias_ids = [int(c) for c in categorias_seleccionadas if c.isdigit()]
        ventas_ids = VentaItem.objects.filter(producto__categoria__id__in=categorias_ids).values_list('venta_id', flat=True)
        ventas_qs = ventas_qs.filter(id__in=ventas_ids)

    # --- Ventas por fecha ---
    # Solo aplicar filtros de fecha
    ventas_fecha_qs = Venta.objects.filter(anulada=False)
    if fecha_desde:
        ventas_fecha_qs = ventas_fecha_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        ventas_fecha_qs = ventas_fecha_qs.filter(fecha__lte=fecha_hasta)

    from collections import defaultdict
    ventas_por_fecha_dict = defaultdict(float)
    ventas = ventas_fecha_qs.prefetch_related('items')
    for venta in ventas:
        total_venta = 0.0
        for item in venta.items.all():
            cantidad = float(item.cantidad)
            precio = float(item.precio or 0)
            descuento_pct = float(item.descuento or 0)
            subtotal = cantidad * precio
            descuento = subtotal * (descuento_pct / 100)
            total_venta += subtotal - descuento
        ventas_por_fecha_dict[venta.fecha] += total_venta
    # Ordenar fechas correctamente y asegurar que todas sean string para el template
    fechas_ventas_activas = []
    montos_ventas_activas = []
    for k, v in sorted(ventas_por_fecha_dict.items()):
        if v > 0:
            fechas_ventas_activas.append(k.strftime('%Y-%m-%d'))
            montos_ventas_activas.append(v)
    # --- Ventas por vendedor ---
    ventas_por_vendedor = ventas_qs.filter(anulada=False).values('vendedor').annotate(total=Count('id'))
    # --- Ventas por categoría ---
    ventas_por_categoria = VentaItem.objects.filter(venta__in=ventas_qs)
    ventas_por_categoria = ventas_por_categoria.values('producto__categoria__nombre').annotate(total=Sum('precio'))

    # --- Ventas activas vs canceladas ---
    total_ventas = ventas_qs.count()
    ventas_activas = ventas_qs.filter(anulada=False).count()
    ventas_canceladas = ventas_qs.filter(anulada=True).count()

    # --- Notas de crédito ---
    notas_credito_qs = NotaCredito.objects.all()
    if fecha_desde:
        notas_credito_qs = notas_credito_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        notas_credito_qs = notas_credito_qs.filter(fecha__lte=fecha_hasta)
    if categorias_seleccionadas and 'todas' not in categorias_seleccionadas:
        notas_ids = NotaCreditoItem.objects.filter(producto__categoria__id__in=categorias_seleccionadas).values_list('nota_id', flat=True)
        notas_credito_qs = notas_credito_qs.filter(id__in=notas_ids)
    cantidad_notas_credito = notas_credito_qs.count()
    if cantidad_notas_credito > 0:
        total_saldos_nc = sum(nota.total for nota in notas_credito_qs)
        promedio_saldo_notas = float(total_saldos_nc) / cantidad_notas_credito
    else:
        promedio_saldo_notas = 0.0

    context = {
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'vendedores_seleccionados': vendedores_seleccionados,
        'categorias_seleccionadas': categorias_seleccionadas,
        'vendedores': vendedores,
        'categorias': categorias,
    # BI DATA
    'ventas_por_fecha': fechas_ventas_activas,
    'montos_ventas': montos_ventas_activas,
    'ventas_por_vendedor': list(ventas_por_vendedor),
    'ventas_por_categoria': list(ventas_por_categoria),
    'total_ventas': total_ventas,
    'ventas_activas': ventas_activas,
    'ventas_canceladas': ventas_canceladas,
    'cantidad_notas_credito': cantidad_notas_credito,
    'promedio_saldo_notas': float(promedio_saldo_notas),
    }
    return render(request, 'reportes/rep_ventas_generales.html', context)


@login_required
def proyeccion_api(request):
    """API AJAX: devuelve una proyección simple de ventas.

    Parámetros GET:
      - fecha_desde, fecha_hasta (YYYY-MM-DD)
      - vendedores (lista de ids o nombres)
      - categorias (lista de ids)
      - horizonte (int) número de días a proyectar
    """
    from datetime import datetime, timedelta
    from ventas.models import Venta, VentaItem
    from django.db.models import Sum

    # Parse dates
    fecha_desde_str = request.GET.get('fecha_desde')
    fecha_hasta_str = request.GET.get('fecha_hasta')
    try:
        fecha_desde = datetime.strptime(fecha_desde_str, '%Y-%m-%d').date() if fecha_desde_str else None
    except Exception:
        fecha_desde = None
    try:
        fecha_hasta = datetime.strptime(fecha_hasta_str, '%Y-%m-%d').date() if fecha_hasta_str else None
    except Exception:
        fecha_hasta = None

    vendedores = request.GET.getlist('vendedores')
    categorias = request.GET.getlist('categorias')
    horizonte = int(request.GET.get('horizonte', 30))

    ventas_qs = Venta.objects.filter(anulada=False)
    if fecha_desde:
        ventas_qs = ventas_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        ventas_qs = ventas_qs.filter(fecha__lte=fecha_hasta)
    # Filtrado vendedores (campo vendedor es string en este proyecto)
    if vendedores and 'todos' not in vendedores:
        vendedores_nombres = [v for v in vendedores if v != 'todos']
        ventas_qs = ventas_qs.filter(vendedor__in=vendedores_nombres)
    # Filtrado categorias
    if categorias and 'todas' not in categorias:
        categorias_ids = [int(c) for c in categorias if c.isdigit()]
        ventas_ids = VentaItem.objects.filter(producto__categoria__id__in=categorias_ids).values_list('venta_id', flat=True)
        ventas_qs = ventas_qs.filter(id__in=ventas_ids)


    from collections import defaultdict
    from decimal import Decimal
    ventas_por_fecha = defaultdict(Decimal)
    ventas = ventas_qs.prefetch_related('items')

    for venta in ventas:
        try:
            total_venta = venta.total
        except Exception:

            total_venta = Decimal('0')
            for item in venta.items.all():
                try:
                    precio = Decimal(str(item.precio or 0))
                except Exception:
                    precio = Decimal('0')
                try:
                    cantidad = Decimal(str(item.cantidad or 0))
                except Exception:
                    cantidad = Decimal('0')
                try:
                    descuento_pct = Decimal(str(item.descuento or 0))
                except Exception:
                    descuento_pct = Decimal('0')
                subtotal = precio * cantidad
                descuento = subtotal * (descuento_pct / Decimal('100'))
                total_venta += subtotal - descuento
        ventas_por_fecha[venta.fecha] += total_venta

    if ventas_por_fecha:
        min_fecha = min(ventas_por_fecha.keys())
        max_fecha = max(ventas_por_fecha.keys())
    else:

        today = datetime.today().date()
        min_fecha = today - timedelta(days=30)
        max_fecha = today

    fecha = min_fecha
    series_dates = []
    series_values = []
    while fecha <= max_fecha:
        series_dates.append(fecha.strftime('%Y-%m-%d'))

        val = ventas_por_fecha.get(fecha, Decimal('0'))
        try:
            fv = float(round(val, 2))
        except Exception:
            fv = float(val)
        series_values.append(fv)
        fecha += timedelta(days=1)


    nonzero_days = sum(1 for v in series_values if v and v > 0)
    if nonzero_days < 3:

        lookback_days = 90
        fallback_start = max_fecha - timedelta(days=lookback_days)
        ventas_fb = Venta.objects.filter(anulada=False, fecha__gte=fallback_start, fecha__lte=max_fecha).prefetch_related('items')
        ventas_por_fecha_fb = defaultdict(Decimal)
        for venta in ventas_fb:
            try:
                total_venta = venta.total
            except Exception:
                total_venta = Decimal('0')
                for item in venta.items.all():
                    try:
                        precio = Decimal(str(item.precio or 0))
                    except Exception:
                        precio = Decimal('0')
                    try:
                        cantidad = Decimal(str(item.cantidad or 0))
                    except Exception:
                        cantidad = Decimal('0')
                    try:
                        descuento_pct = Decimal(str(item.descuento or 0))
                    except Exception:
                        descuento_pct = Decimal('0')
                    subtotal = precio * cantidad
                    descuento = subtotal * (descuento_pct / Decimal('100'))
                    total_venta += subtotal - descuento
            ventas_por_fecha_fb[venta.fecha] += total_venta


        fecha = fallback_start
        series_dates = []
        series_values = []
        while fecha <= max_fecha:
            series_dates.append(fecha.strftime('%Y-%m-%d'))
            val = ventas_por_fecha_fb.get(fecha, Decimal('0'))
            try:
                fv = float(round(val, 2))
            except Exception:
                fv = float(val)
            series_values.append(fv)
            fecha += timedelta(days=1)

    window = 14 if len(series_values) >= 14 else max(1, len(series_values))
    import statistics
    if len(series_values) == 0:
        mean_recent = 0.0
    else:
        mean_recent = statistics.mean(series_values[-window:])


    projected_dates = []
    projected_values = []
    for i in range(1, horizonte + 1):
        d = max_fecha + timedelta(days=i)
        projected_dates.append(d.strftime('%Y-%m-%d'))

        projected_values.append(round(mean_recent, 2))


    scale = 1
    try:
        overall_mean = statistics.mean(series_values) if series_values else 0
    except Exception:
        overall_mean = 0
    if overall_mean and overall_mean > 100000:

        scale = 100
        series_values = [round(v / scale, 2) for v in series_values]
        projected_values = [round(v / scale, 2) for v in projected_values]

    return JsonResponse({
        'historical': {'dates': series_dates, 'values': series_values},
        'projected': {'dates': projected_dates, 'values': projected_values},
        'meta': {'horizonte': horizonte, 'window': window, 'scale_divided_by': scale}
    })


def categorias_api(request):
    categorias = Categoria.objects.all().order_by('nombre')
    data = [{'id': c.id, 'nombre': c.nombre} for c in categorias]
    return JsonResponse({'categorias': data})

def categorias_api(request):
    categorias = Categoria.objects.all().order_by('nombre')
    data = [{'id': c.id, 'nombre': c.nombre} for c in categorias]
    return JsonResponse({'categorias': data})