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
    vendedor_map = {str(v['id']): v['nombre'] for v in vendedores}

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
        selected_ids = [v for v in vendedores_seleccionados if v != 'todos']
        vendedor_nombres = [vendedor_map.get(v) for v in selected_ids if v in vendedor_map]
        if vendedor_nombres:
            ventas_qs = ventas_qs.filter(vendedor__in=vendedor_nombres)

    # Filtrado categorías
    if categorias_seleccionadas and 'todas' not in categorias_seleccionadas:
        categorias_ids = [int(c) for c in categorias_seleccionadas if str(c).isdigit()]
        if categorias_ids:
            ventas_ids = VentaItem.objects.filter(producto__categoria__id__in=categorias_ids).values_list('venta_id', flat=True)
            ventas_qs = ventas_qs.filter(id__in=ventas_ids)

    # --- Ventas por fecha/vendedor/categoría ---
    from collections import defaultdict
    ventas_por_fecha_dict = defaultdict(float)
    ventas_por_vendedor_dict = defaultdict(float)
    ventas_por_categoria_dict = defaultdict(float)
    # count unidades vendidas por categoría (solo ventas activas)
    ventas_por_categoria_count = defaultdict(float)
    total_ventas_monto = 0.0

    ventas = ventas_qs.prefetch_related('items', 'notas_credito')
    total_ventas_monto = 0.0
    for venta in ventas:
        total_venta = 0.0
        for item in venta.items.all():
            try:
                cantidad = float(item.cantidad or 0)
            except Exception:
                cantidad = 0.0
            try:
                precio = float(item.precio or 0)
            except Exception:
                precio = 0.0
            try:
                descuento_pct = float(item.descuento or 0)
            except Exception:
                descuento_pct = 0.0
            subtotal = cantidad * precio
            descuento = subtotal * (descuento_pct / 100)
            linea_total = subtotal - descuento
            total_venta += linea_total
            if not getattr(venta, 'anulada', False) and not (getattr(venta, 'notas_credito', None) and venta.notas_credito.exists()):
                cat_nombre = getattr(item.producto.categoria, 'nombre', 'Sin categoría') if getattr(item, 'producto', None) else 'Sin categoría'
                ventas_por_categoria_dict[cat_nombre] += linea_total
                try:
                    ventas_por_categoria_count[cat_nombre] += float(item.cantidad or 0)
                except Exception:
                    pass

        has_nota = getattr(venta, 'notas_credito', None) and venta.notas_credito.exists()
        anulada = getattr(venta, 'anulada', False)
        if not anulada and not has_nota:
            ventas_por_fecha_dict[venta.fecha] += total_venta
            ventas_por_vendedor_dict[getattr(venta, 'vendedor', 'Sin vendedor')] += total_venta
            total_ventas_monto += total_venta

    ventas_por_vendedor = [{'vendedor': k, 'total': v} for k, v in ventas_por_vendedor_dict.items()]
    # --- Ventas por categoría (convertir a lista con total monetario) ---
    ventas_por_categoria = [{'producto__categoria__nombre': k, 'total': v} for k, v in ventas_por_categoria_dict.items()]
    # unidades vendidas por categoría (para gráfico de unidades)
    ventas_por_categoria_unidades = [{'categoria': k, 'cantidad': v} for k, v in ventas_por_categoria_count.items()]

    total_ventas = ventas_qs.count()
    ventas_canceladas = 0
    ventas_activas = total_ventas

    total_monto_ventas = float(total_ventas_monto or 0.0)

    # --- Notas de crédito ---
    notas_credito_qs = NotaCredito.objects.all()
    if fecha_desde:
        notas_credito_qs = notas_credito_qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        notas_credito_qs = notas_credito_qs.filter(fecha__lte=fecha_hasta)
    if categorias_seleccionadas and 'todas' not in categorias_seleccionadas:
        categorias_ids_for_nc = [int(c) for c in categorias_seleccionadas if str(c).isdigit()]
        if categorias_ids_for_nc:
            notas_ids = NotaCreditoItem.objects.filter(producto__categoria__id__in=categorias_ids_for_nc).values_list('nota_id', flat=True)
            notas_credito_qs = notas_credito_qs.filter(id__in=notas_ids)
    cantidad_notas_credito = notas_credito_qs.count()
    if cantidad_notas_credito > 0:
        total_saldos_nc = sum(float(nota.total) for nota in notas_credito_qs)

    else:
        total_saldos_nc = 0.0

    total_monto_notas = float(total_saldos_nc or 0.0)
    neto_total = total_monto_ventas - total_monto_notas

    total_ventas_bruto = total_monto_ventas + total_monto_notas

    promedio_saldo_notas = float(neto_total)


    from collections import defaultdict as _dd
    notas_por_fecha_dict = _dd(float)
    for nota in notas_credito_qs:
        try:
            fecha_n = nota.fecha
            notas_por_fecha_dict[fecha_n] += float(nota.total)
        except Exception:
            continue

    # Ahora construimos listas ordenadas de fechas y montos netos (ventas - notas por fecha)
    fechas_ventas_activas = []
    montos_ventas_activas = []
    for k, v in sorted(ventas_por_fecha_dict.items()):
        notas_val = notas_por_fecha_dict.get(k, 0.0)
        neto = v - notas_val
        fechas_ventas_activas.append(k.strftime('%Y-%m-%d'))
        montos_ventas_activas.append(neto)

    # Finalizar cálculo de ventas canceladas usando notas filtradas
    # Obtener IDs de ventas referenciadas por notas, pero limitarlas a las ventas dentro del queryset filtrado
    venta_ids_from_notas_all = set(x for x in notas_credito_qs.values_list('venta_original_id', flat=True) if x)
    venta_ids_in_ventas_qs = set(ventas_qs.values_list('id', flat=True))
    # Sólo considerar las ventas que están en el rango/filtros actuales
    venta_ids_from_notas = venta_ids_from_notas_all & venta_ids_in_ventas_qs
    anuladas_in_ventas = set(ventas_qs.filter(anulada=True).values_list('id', flat=True))
    ventas_canceladas_ids = venta_ids_from_notas | anuladas_in_ventas
    ventas_canceladas = cantidad_notas_credito
    ventas_activas_qs = ventas_qs.filter(anulada=False).exclude(id__in=venta_ids_from_notas)
    ventas_activas = ventas_activas_qs.count()
    ventas_activas_ids = list(ventas_activas_qs.values_list('id', flat=True))

    context = {
        'fecha_desde': fecha_desde.strftime('%Y-%m-%d') if fecha_desde else '',
        'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d') if fecha_hasta else '',
        'vendedores_seleccionados': vendedores_seleccionados,
        'categorias_seleccionadas': categorias_seleccionadas,
        'vendedores': vendedores,
        'categorias': categorias,
    # BI DATA
    'ventas_por_fecha': fechas_ventas_activas,
    'montos_ventas': montos_ventas_activas,
    'ventas_por_vendedor': ventas_por_vendedor,
    'ventas_por_categoria': ventas_por_categoria,
    'ventas_por_categoria_unidades': ventas_por_categoria_unidades,
    'total_ventas': total_ventas,
    'ventas_activas': ventas_activas,
    'ventas_canceladas': ventas_canceladas,
    'cantidad_notas_credito': cantidad_notas_credito,
    'promedio_saldo_notas': float(promedio_saldo_notas),
    'total_monto_ventas': round(total_monto_ventas, 2),
    'total_monto_notas': round(total_monto_notas, 2),
    'neto_total': round(neto_total, 2),
    'total_ventas_bruto': round(total_ventas_bruto, 2),
    }
    try:
        logger.info("rep_ventas_generales: params fecha_desde=%s fecha_hasta=%s vendedores=%s categorias=%s", fecha_desde_str, fecha_hasta_str, vendedores_seleccionados, categorias_seleccionadas)
        logger.info("rep_ventas_generales: total_ventas=%s ventas_activas=%s ventas_canceladas=%s cantidad_notas=%s venta_ids_from_notas=%s total_monto_ventas=%s total_monto_notas=%s neto_total=%s", total_ventas, ventas_activas, ventas_canceladas, cantidad_notas_credito, list(venta_ids_from_notas), total_monto_ventas, total_monto_notas, neto_total)
    except Exception:
        pass
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