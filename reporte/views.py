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
import logging

logger = logging.getLogger(__name__)

def dashboard_view(request):
    return render(request, 'reportes/index_report.html')

def rep_ventas_generales_view(request):
    
    # Calcular el monto total de notas de crédito emitidas en el rango de fechas seleccionado (sin excluir por venta original)
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
    # --- Ventas por categoría (precio*cantidad, solo ventas activas y rango de fecha) ---
    from django.db.models import F, FloatField, ExpressionWrapper
    ventas_activas_qs = ventas_qs.filter(anulada=False)
    ventas_items = VentaItem.objects.filter(venta__in=ventas_activas_qs)
    ventas_por_categoria = ventas_items.values('producto__categoria__nombre').annotate(
        total=Sum(ExpressionWrapper(F('precio') * F('cantidad'), output_field=FloatField()))
    ).order_by('-total')

    # --- Ventas activas vs canceladas ---
    total_ventas = 0.0
    ventas_activas = ventas_qs.filter(anulada=False).count()
    ventas_canceladas = ventas_qs.filter(anulada=True).count()
    # Calcular el total de ventas (sumando los montos de cada venta)
    ventas_montos_qs = ventas_qs.prefetch_related('items')
    for venta in ventas_montos_qs:
        for item in venta.items.all():
            cantidad = float(item.cantidad)
            precio = float(item.precio or 0)
            descuento_pct = float(item.descuento or 0)
            subtotal = cantidad * precio
            descuento = subtotal * (descuento_pct / 100)
            total_ventas += subtotal - descuento

    # --- Notas de crédito ---
    notas_credito_qs = NotaCredito.objects.all()
    if fecha_desde:
        notas_credito_qs = notas_credito_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        notas_credito_qs = notas_credito_qs.filter(fecha__lte=fecha_hasta)
    # Excluir las notas de crédito cuya venta asociada esté en el rango de fechas seleccionado
    if fecha_desde and fecha_hasta:
        notas_credito_qs = notas_credito_qs.exclude(venta_original__fecha__gte=fecha_desde, venta_original__fecha__lte=fecha_hasta)
    elif fecha_desde:
        notas_credito_qs = notas_credito_qs.exclude(venta_original__fecha__gte=fecha_desde)
    elif fecha_hasta:
        notas_credito_qs = notas_credito_qs.exclude(venta_original__fecha__lte=fecha_hasta)
    if categorias_seleccionadas and 'todas' not in categorias_seleccionadas:
        categorias_ids_nc = [int(c) for c in categorias_seleccionadas if c.isdigit()]
        notas_ids = NotaCreditoItem.objects.filter(producto__categoria__id__in=categorias_ids_nc).values_list('nota_id', flat=True)
        notas_credito_qs = notas_credito_qs.filter(id__in=notas_ids)
    cantidad_notas_credito = notas_credito_qs.count()
    total_saldos_nc = sum(nota.total for nota in notas_credito_qs) if cantidad_notas_credito > 0 else 0.0
    promedio_saldo_bruto = float(total_ventas) + float(total_saldos_nc)
    # Sumatoria del total de cada nota de crédito en notas_credito_qs
    notas_credito_rango_qs = NotaCredito.objects.all()
    if fecha_desde:
        notas_credito_rango_qs = notas_credito_rango_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        notas_credito_rango_qs = notas_credito_rango_qs.filter(fecha__lte=fecha_hasta)
    if categorias_seleccionadas and 'todas' not in categorias_seleccionadas:
        categorias_ids_nc = [int(c) for c in categorias_seleccionadas if c.isdigit()]
        notas_ids = NotaCreditoItem.objects.filter(producto__categoria__id__in=categorias_ids_nc).values_list('nota_id', flat=True)
        notas_credito_rango_qs = notas_credito_rango_qs.filter(id__in=notas_ids)
    monto_total_notas_credito_rango = sum(float(nota.total) for nota in notas_credito_rango_qs)
   

    # Eliminar línea incorrecta, ya que los filtros de fecha ya están aplicados correctamente arriba
    monto_total_notas_credito_rango = 0.0
    for nota in notas_credito_qs:
        monto_total_notas_credito_rango += float(nota.total)
    ventas_activas_rango_qs = Venta.objects.filter(anulada=False)
    if fecha_desde:
        ventas_activas_rango_qs = ventas_activas_rango_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        ventas_activas_rango_qs = ventas_activas_rango_qs.filter(fecha__lte=fecha_hasta)
    if vendedores_seleccionados and 'todos' not in vendedores_seleccionados:
        vendedores_nombres = [v for v in vendedores_seleccionados if v != 'todos']
        ventas_activas_rango_qs = ventas_activas_rango_qs.filter(vendedor__in=vendedores_nombres)
    if categorias_seleccionadas and 'todas' not in categorias_seleccionadas:
        categorias_ids = [int(c) for c in categorias_seleccionadas if c.isdigit()]
        ventas_ids = VentaItem.objects.filter(producto__categoria__id__in=categorias_ids).values_list('venta_id', flat=True)
        ventas_activas_rango_qs = ventas_activas_rango_qs.filter(id__in=ventas_ids)
    monto_total_ventas_activas_rango = 0.0
    for venta in ventas_activas_rango_qs.prefetch_related('items'):
        for item in venta.items.all():
            cantidad = float(item.cantidad)
            precio = float(item.precio or 0)
            descuento_pct = float(item.descuento or 0)
            subtotal = cantidad * precio
            descuento = subtotal * (descuento_pct / 100)
            monto_total_ventas_activas_rango += subtotal - descuento
    # Obtener parámetros GET
    notas_credito_qs = NotaCredito.objects.all()
    if fecha_desde:
        notas_credito_qs = notas_credito_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        notas_credito_qs = notas_credito_qs.filter(fecha__lte=fecha_hasta)
    total_notas_credito_qs = sum(float(nota.total) for nota in notas_credito_qs)
    promedio_saldo_notas = float(monto_total_ventas_activas_rango) - float(total_notas_credito_qs)
    import json
    ventas_categoria_labels = [v['producto__categoria__nombre'] for v in ventas_por_categoria]
    ventas_categoria_data = [float(v['total']) if v['total'] is not None else 0 for v in ventas_por_categoria]
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
        'ventas_categoria_labels_json': json.dumps(ventas_categoria_labels, ensure_ascii=False),
        'ventas_categoria_data_json': json.dumps(ventas_categoria_data),
        'total_ventas': total_ventas,
        'ventas_activas': ventas_activas,
        'ventas_canceladas': ventas_canceladas,
        'promedio_saldo_bruto': promedio_saldo_bruto,
        'promedio_saldo_notas': float(promedio_saldo_notas),
        'total_saldos_nc': float(total_saldos_nc),
        'total_notas_credito_qs': float(total_notas_credito_qs),
    }
    return render(request, 'reportes/rep_ventas_generales.html', context)

# API para obtener categorías de productos
def categorias_api(request):
    categorias = Categoria.objects.all().order_by('nombre')
    data = [{'id': c.id, 'nombre': c.nombre} for c in categorias]
    return JsonResponse({'categorias': data})

# API para obtener categorías de productos
def categorias_api(request):
    categorias = Categoria.objects.all().order_by('nombre')
    data = [{'id': c.id, 'nombre': c.nombre} for c in categorias]
    return JsonResponse({'categorias': data})