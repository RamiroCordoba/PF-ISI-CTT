from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import ClienteForm
from django.views.decorators.http import require_POST
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from productos.models import Producto,Proveedor
from django.db.models import Q
from django.views import View
from decimal import Decimal, InvalidOperation
from django.template.loader import render_to_string
import pdfkit
import qrcode
import io
from django.http import HttpResponse
import logging

class IvaList(LoginRequiredMixin, ListView):
    model = Iva
    template_name = "iva/iva_list.html"
    context_object_name = "ivas"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")

        buscar = self.request.GET.get("buscar", "").strip()
        estados = self.request.GET.getlist("estado") 

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        if estados:
            if "activo" in estados and "inactivo" in estados:

                pass
            elif "activo" in estados:
                queryset = queryset.filter(activo=True)
            elif "inactivo" in estados:
                queryset = queryset.filter(activo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buscar"] = self.request.GET.get("buscar", "")
        context["filtro_estados"] = self.request.GET.getlist("estado")  
        return context


  
class IvaCreate(LoginRequiredMixin,CreateView):
     model=Iva
     fields = ["nombre", "porcentaje", "activo"]
     template_name="iva/iva_form.html"
     success_url = reverse_lazy("mis_iva")
     
class IvaUpdate(LoginRequiredMixin,UpdateView):
     model=Iva
     fields = ["nombre", "porcentaje", "activo"]
     template_name="iva/iva_form.html"
     success_url = reverse_lazy("mis_iva")

class IvaDelete(LoginRequiredMixin,DeleteView):
     model=Iva
     template_name="iva/iva_confirm_delete.html"
     success_url = reverse_lazy("mis_iva")

class IvaDetail(DetailView):
     model=Iva
     template_name="iva/iva_details.html"
     context_object_name = 'iva'


class MonedaList(LoginRequiredMixin, ListView):
    model = Moneda
    template_name = "moneda/moneda_list.html"
    context_object_name = "monedas"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")

        buscar = self.request.GET.get("buscar", "").strip()
        estados = self.request.GET.getlist("estado")  

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        if estados:
            if "activo" in estados and "inactivo" in estados:
                pass
            elif "activo" in estados:
                queryset = queryset.filter(activo=True)
            elif "inactivo" in estados:
                queryset = queryset.filter(activo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buscar"] = self.request.GET.get("buscar", "")
        context["filtro_estados"] = self.request.GET.getlist("estado")  
        return context


  
class MonedaCreate(LoginRequiredMixin,CreateView):
     model=Moneda
     fields = ["nombre", "simbolo", "activo"]
     template_name="moneda/moneda_form.html"
     success_url = reverse_lazy("mis_monedas")
     
class MonedaUpdate(LoginRequiredMixin,UpdateView):
     model=Moneda
     fields = ["nombre", "simbolo", "activo"]
     template_name="moneda/moneda_form.html"
     success_url = reverse_lazy("mis_monedas")

class MonedaDelete(LoginRequiredMixin,DeleteView):
     model=Moneda
     template_name="moneda/moneda_confirm_delete.html"
     success_url = reverse_lazy("mis_monedas")

class MonedaDetail(DetailView):
     model=Moneda
     template_name="moneda/moneda_details.html"
     context_object_name = 'moneda'

class CondicionFiscalList(LoginRequiredMixin, ListView):
    model = CondicionFiscal
    template_name = "condicionfiscal/condicionfiscal_list.html"
    context_object_name = "condicionesFiscales"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")

        buscar = self.request.GET.get("buscar", "").strip()
        estados = self.request.GET.getlist("estado")  

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        if estados:
            if "activo" in estados and "inactivo" in estados:
                pass
            elif "activo" in estados:
                queryset = queryset.filter(activo=True)
            elif "inactivo" in estados:
                queryset = queryset.filter(activo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buscar"] = self.request.GET.get("buscar", "")
        context["filtro_estados"] = self.request.GET.getlist("estado")  
        return context


  
class CondicionFiscalCreate(LoginRequiredMixin,CreateView):
     model=CondicionFiscal
     fields = ["nombre", "activo"]
     template_name="condicionFiscal/condicionfiscal_form.html"
     success_url = reverse_lazy("mis_condiciones_fiscales")
     
class CondicionFiscalUpdate(LoginRequiredMixin,UpdateView):
     model=CondicionFiscal
     fields = ["nombre", "activo"]
     template_name="condicionFiscal/condicionfiscal_form.html"
     success_url = reverse_lazy("mis_condiciones_fiscales")

class CondicionFiscalDelete(LoginRequiredMixin,DeleteView):
     model=CondicionFiscal
     template_name="condicionFiscal/condicionfiscal_confirm_delete.html"
     success_url = reverse_lazy("mis_condiciones_fiscales")

class CondicionFiscalDetail(DetailView):
     model=CondicionFiscal
     template_name="condicionFiscal/condicionfiscal_details.html"
     context_object_name = 'condicionFiscal'


class ClienteList(LoginRequiredMixin, ListView):

    model = Cliente
    template_name = "cliente/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")

        buscar = self.request.GET.get("buscar", "").strip()
        estados = self.request.GET.getlist("estado")  

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        if estados:
            if "activo" in estados and "inactivo" in estados:
                pass
            elif "activo" in estados:
                queryset = queryset.filter(activo=True)
            elif "inactivo" in estados:
                queryset = queryset.filter(activo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        queryset = self.get_queryset()
        from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('page')
        try:
            clientes_paginated = paginator.page(page)
        except PageNotAnInteger:
            clientes_paginated = paginator.page(1)
        except EmptyPage:
            clientes_paginated = paginator.page(paginator.num_pages)

        context["page_obj"] = clientes_paginated
        context["clientes"] = clientes_paginated.object_list
        context["buscar"] = request.GET.get("buscar", "")
        context["filtro_estados"] = request.GET.getlist("estado")  
        context['request'] = request
        context['filtros_activos'] = any([
            request.GET.getlist('estado'),
            request.GET.get('buscar')
        ])
        return context


  
class ClienteCreate(LoginRequiredMixin,CreateView):
     model=Cliente
     form_class = ClienteForm
     template_name="cliente/cliente_form.html"
     success_url = reverse_lazy("mis_clientes")
     
class ClienteUpdate(LoginRequiredMixin,UpdateView):
     model=Cliente
     form_class = ClienteForm
     template_name="cliente/cliente_form.html"
     success_url = reverse_lazy("mis_clientes")

class ClienteDelete(LoginRequiredMixin,DeleteView):
     model=Cliente
     template_name="cliente/cliente_confirm_delete.html"
     success_url = reverse_lazy("mis_clientes")

class ClienteDetail(DetailView):
     model=Cliente
     template_name="cliente/cliente_details.html"
     context_object_name = 'cliente'



class VentaList(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('cliente', 'moneda', 'forma_pago', 'iva')
        request = self.request

        # Filtros
        filtro_estados = request.GET.getlist('estado')
        filtro_proveedores = request.GET.getlist('proveedor')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        buscar = request.GET.get('buscar')

        # Estado completado
        if filtro_estados:
            estado_q = Q()
            if "completado" in filtro_estados:
                estado_q |= Q(completado=True)
            if "pendiente" in filtro_estados:
                estado_q |= Q(completado=False)
            qs = qs.filter(estado_q)

        # Proveedores
        if filtro_proveedores:
            qs = qs.filter(cliente__id__in=filtro_proveedores)

        # Fechas
        if fecha_inicio:
            qs = qs.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(fecha__lte=fecha_fin)

        # Buscador
        if buscar:
            qs = qs.filter(
                Q(comentarios__icontains=buscar) |
                Q(cliente__nombre__icontains=buscar) |
                Q(cliente__apellido__icontains=buscar)
            )

        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        context.update({
            'proveedores': Proveedor.objects.all(),
            'filtro_estados': request.GET.getlist('estado'),
            'filtro_proveedores': request.GET.getlist('proveedor'),
            'filtros_activos': any([
                request.GET.getlist('estado'),
                request.GET.getlist('proveedor'),
                request.GET.get('fecha_inicio'),
                request.GET.get('fecha_fin'),
                request.GET.get('buscar')
            ]),
            'request': request
        })

        return context

@require_POST
@csrf_exempt
def ajax_nuevo_cliente(request):
    form = ClienteForm(request.POST)
    if form.is_valid():
        cliente = form.save()
        nombre = cliente.razon_social or f"{cliente.nombre} {cliente.apellido}".strip()
        return JsonResponse({'id': cliente.id, 'nombre': nombre})
    else:
        errores = []
        for field, msgs in form.errors.items():
            for msg in msgs:
                errores.append(f"<div>{msg}</div>")
        return JsonResponse({'errors': ''.join(errores)}, status=400)

class NotaCreditoList(LoginRequiredMixin, ListView):
    model = NotaCredito
    template_name = 'notacredito/notacredito_list.html'
    context_object_name = 'notas'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('cliente', 'venta_original')
        buscar = self.request.GET.get('buscar')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        if fecha_inicio:
            qs = qs.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(fecha__lte=fecha_fin)
        if buscar:
            qs = qs.filter(
                Q(comentarios__icontains=buscar) |
                Q(cliente__nombre__icontains=buscar) |
                Q(cliente__apellido__icontains=buscar)
            )
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        request = self.request
        # Paginacion de notas de crédito
        queryset = self.get_queryset()
        from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('page')
        try:
            notas_paginated = paginator.page(page)
        except PageNotAnInteger:
            notas_paginated = paginator.page(1)
        except EmptyPage:
            notas_paginated = paginator.page(paginator.num_pages)

        ctx["page_obj"] = notas_paginated
        ctx["notas"] = notas_paginated.object_list
        ctx['request'] = request
        ctx['filtros_activos'] = any([
            request.GET.get('fecha_inicio'),
            request.GET.get('fecha_fin'),
            request.GET.get('buscar')
        ])
        return ctx


class NotaCreditoDetail(LoginRequiredMixin, DetailView):
    model = NotaCredito
    template_name = 'notacredito/notacredito_details.html'
    context_object_name = 'nota'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = self.object.items.select_related('producto')
        total = Decimal('0')
        enriched = []
        for it in items:
            precio = Decimal(str(it.precio)) if it.precio is not None else Decimal('0')
            cantidad = Decimal(str(it.cantidad)) if it.cantidad is not None else Decimal('0')
            descuento_pct = Decimal(str(it.descuento or 0))
            descuento_factor = Decimal('1') - (descuento_pct / Decimal('100'))
            subtotal = (precio * cantidad * descuento_factor)
            total += subtotal
            enriched.append((it, subtotal))
        ctx['items'] = enriched
        ctx['total'] = total
        return ctx

def autocomplete_productos2(request):
    term = request.GET.get("term", "")
    proveedor_id = request.GET.get("proveedor_id")

    productos = Producto.objects.filter(nombre__icontains=term)

    if proveedor_id:  
        productos = productos.filter(proveedores__id=proveedor_id)

    productos = productos[:20]

    results = [
        {
            "id": p.id,
            "value": p.nombre,       
            "precio": float(p.precio) if p.precio else 0
        } 
        for p in productos
    ]
    return JsonResponse(results, safe=False)


def autocomplete_clientes(request):
    term = request.GET.get('term', '').strip()
    qs = Cliente.objects.all()
    if term:
        qs = qs.filter(
            Q(razon_social__icontains=term) |
            Q(nombre__icontains=term) |
            Q(apellido__icontains=term)
        )
    qs = qs.order_by('razon_social', 'nombre')[:20]

    results = []
    for c in qs:
        display = c.razon_social if c.razon_social else (f"{c.nombre} {c.apellido}".strip())
        results.append({
            'id': c.id,
            'value': display,
            'label': display,
            'text': display,
        })
    return JsonResponse(results, safe=False)

def autocomplete_formas_pago(request):
    term = request.GET.get('term', '').strip()
    qs = FormaPago.objects.all()
    if term:
        qs = qs.filter(Q(nombre__icontains=term) | Q(descripcion__icontains=term))
    qs = qs.order_by('nombre')[:20]
    results = []
    for f in qs:
        label = getattr(f, 'nombre', None) or getattr(f, 'descripcion', str(f))
        results.append({
            'id': f.id,
            'value': label,
            'label': label,
        })
    return JsonResponse(results, safe=False)

def productos_por_proveedor2(request):
    proveedor_id = request.GET.get('proveedor_id')
    
    if not proveedor_id:
        return JsonResponse({'productos': []})

    productos = (
        Producto.objects
        .filter(proveedores__id=proveedor_id)
        .values('id', 'nombre')
        .order_by('nombre')
    )

    return JsonResponse({'productos': list(productos)})


def ventas_por_cliente(request):
    cliente_id = request.GET.get('cliente_id')
    if not cliente_id:
        return JsonResponse({'ventas': []})
    ventas = Venta.objects.filter(cliente_id=cliente_id, anulada=False).order_by('-id')[:100]
    data = [{'id': v.id, 'display': f"#{v.id} - {getattr(v.cliente,'nombre','')} ({v.fecha})", 'fecha': v.fecha.strftime('%d/%m/%Y') if getattr(v, 'fecha', None) else '', 'total': str(getattr(v, 'total', '') or '')} for v in ventas]
    return JsonResponse(data, safe=False)


@require_POST
def crear_nota_desde_venta(request):
    """Create a NotaCredito from a Venta (given venta id) and return JSON result."""
    venta_id = request.POST.get('venta_original') or request.POST.get('venta')
    if not venta_id:
        return JsonResponse({'error': 'venta id requerido'}, status=400)
    try:
        venta = Venta.objects.get(pk=venta_id)
    except Venta.DoesNotExist:
        return JsonResponse({'error': 'venta no encontrada'}, status=404)

    # Do not create nota for anuladas ventas
    if getattr(venta, 'anulada', False):
        return JsonResponse({'error': 'venta anulada'}, status=400)

    comentarios = request.POST.get('comentarios', '')
    try:
        from .models import create_nota_from_venta, apply_stock_for_nota
        from django.db import transaction

        nota = None
        applied_count = 0
        with transaction.atomic():
            nota = create_nota_from_venta(venta, comentarios=comentarios)
            if nota is None:
                raise Exception('No se pudo crear la nota de crédito')

            # apply stock for nota (will only apply unapplied items)
            try:
                applied_count = apply_stock_for_nota(nota) or 0
            except Exception:
                # if apply_stock_for_nota fails, raise to rollback
                raise

            # mark venta as anulada
            Venta.objects.filter(pk=venta.pk).update(anulada=True)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'ok': True, 'nota_id': getattr(nota, 'id', None), 'applied_count': applied_count})

class VentaCreate(LoginRequiredMixin, View):
    def get(self, request):

        vendedor_default = request.user.get_full_name() or request.user.username

        try:
            moneda_pesos = Moneda.objects.filter(nombre__iexact='pesos').first()
        except Exception:
            moneda_pesos = None
        initial = {'vendedor': vendedor_default}
        if moneda_pesos:
            initial['moneda'] = moneda_pesos.id
        default_cliente = None
        try:
            default_cliente = Cliente.objects.filter(
                Q(razon_social__icontains='consumidor final') |
                Q(razon_social__icontains='consumidor') |
                Q(nombre__icontains='consumidor') |
                Q(apellido__icontains='consumidor')
            ).order_by('id').first()
            if default_cliente and not initial.get('cliente'):
                initial['cliente'] = default_cliente.id
        except Exception:
            default_cliente = None

        form = VentaForm(initial=initial)
        formset = VentaItemFormSet(instance=Venta())
        context = {
          'form': form,
          'formset': formset,
          'default_cliente_id': getattr(default_cliente, 'id', ''),
          'default_cliente_name': (default_cliente.razon_social if getattr(default_cliente, 'razon_social', None) else (f"{getattr(default_cliente,'nombre','')} {getattr(default_cliente,'apellido','')}") ).strip() if default_cliente else '',
          'formas_pago': FormaPago.objects.all(),
          'default_forma_pago_id': '', 
          'default_forma_pago_name': '', 
          'default_comentarios': initial.get('comentarios', ''),
          'default_moneda_id': getattr(moneda_pesos, 'id', ''),
          'default_moneda_name': getattr(moneda_pesos, 'nombre', '') if moneda_pesos else '',
          'condiciones_fiscales': CondicionFiscal.objects.filter(activo=True).order_by('nombre'),
        }
        return render(request, 'ventas/venta_form.html', context)

    def post(self, request):
        post_data = request.POST.copy()
        vendedor_default = request.user.get_full_name() or request.user.username
        post_data['vendedor'] = vendedor_default
        try:
            moneda_pesos = Moneda.objects.filter(nombre__iexact='pesos').first()
        except Exception:
            moneda_pesos = None
        if moneda_pesos:
            post_data['moneda'] = str(moneda_pesos.id)

        
        if not post_data.get('cliente'):
            try:
                cf = Cliente.objects.filter(
                    Q(razon_social__icontains='consumidor final') |
                    Q(razon_social__icontains='consumidor') |
                    Q(nombre__icontains='consumidor') |
                    Q(apellido__icontains='consumidor')
                ).order_by('id').first()
                if cf:
                    post_data['cliente'] = str(cf.id)
            except Exception:
                pass

        form = VentaForm(post_data)
        if form.is_valid():
            vendedor_default = request.user.get_full_name() or request.user.username
            form.instance.vendedor = vendedor_default
            try:
                if moneda_pesos:
                    form.instance.moneda = moneda_pesos
            except Exception:
                pass
            form.instance.completado = False

            if not form.cleaned_data.get('cliente'):
                try:
                    cf = Cliente.objects.filter(Q(razon_social__iexact='consumidor final') | Q(nombre__iexact='consumidor') | Q(nombre__icontains='consumidor')).first()
                    if cf:
                        form.instance.cliente = cf
                except Exception:
                    pass

            temp_venta = Venta()
            formset = VentaItemFormSet(request.POST, instance=temp_venta)
            if formset.is_valid():
                insuficientes = []
                try:
                    for cd in formset.cleaned_data:
                        if not cd or cd.get('DELETE'):
                            continue
                        producto = cd.get('producto')
                        cantidad = cd.get('cantidad') or 0
                        if producto is None:
                            insuficientes.append((None, 'Producto no seleccionado'))
                            continue
                        prod = Producto.objects.filter(pk=producto.pk).first()
                        if prod is None:
                            insuficientes.append((producto.nombre if producto else '??', 'Producto no encontrado'))
                        else:
                            if prod.stock < cantidad:
                                insuficientes.append((prod.nombre, prod.stock, cantidad))
                except Exception:
                    insuficientes.append(('error', 'No se pudo validar el stock'))

                if insuficientes:
                    msgs = []
                    for it in insuficientes:
                        if len(it) == 3:
                            msgs.append(f"{it[0]}: stock disponible {it[1]}, solicitado {it[2]}")
                        else:
                            msgs.append(str(it))
                    fullmsg = "Stock insuficiente para los siguientes productos: " + "; ".join(msgs)
                    try:
                        form.add_error(None, fullmsg)
                    except Exception:
                        pass
                    messages.error(request, fullmsg)
                    default_cliente_id = post_data.get('cliente') or ''
                    default_cliente_name = ''
                    if default_cliente_id:
                        try:
                            cf_sel = Cliente.objects.filter(pk=default_cliente_id).first()
                            if cf_sel:
                                default_cliente_name = (cf_sel.razon_social if getattr(cf_sel, 'razon_social', None) else (f"{getattr(cf_sel,'nombre','')} {getattr(cf_sel,'apellido','')}")).strip()
                        except Exception:
                            default_cliente_name = ''

                    form = VentaForm(post_data)
                    formset = VentaItemFormSet(request.POST)
                    default_forma_pago_id = post_data.get('forma_pago', '') 
                    default_forma_pago_name = ''
                    if default_forma_pago_id:
                        try:
                            fp = FormaPago.objects.filter(pk=default_forma_pago_id).first()
                            if fp:
                                default_forma_pago_name = getattr(fp, 'nombre', getattr(fp, 'descripcion', str(fp)))
                        except Exception:
                            default_forma_pago_name = ''
                    context = {
                        'form': form,
                        'formset': formset,
                        'stock_errors': msgs,
                        'default_cliente_id': default_cliente_id,
                        'default_cliente_name': default_cliente_name,
                        'formas_pago': FormaPago.objects.all(),
                        'default_forma_pago_id': default_forma_pago_id,
                        'default_forma_pago_name': default_forma_pago_name,
                        'default_comentarios': post_data.get('comentarios', ''),
                        'default_moneda_id': post_data.get('moneda', '') or (getattr(moneda_pesos, 'id', '') if moneda_pesos else ''),
                        'default_moneda_name': '',
                    }
                    return render(request, 'ventas/venta_form.html', context)

                venta = form.save()
                venta.completado = True
                venta.save()
                formset = VentaItemFormSet(request.POST, instance=venta)
                formset.save()
                try:
                    from .models import apply_stock_for_venta
                    apply_stock_for_venta(venta)
                except Exception:
                    pass
                messages.success(request, "Venta creada correctamente.")
                return redirect('mis_ventas')
        else:
            formset = VentaItemFormSet(request.POST)

        default_cliente_id = request.POST.get('cliente') or (getattr(form.instance, 'cliente', None) and getattr(form.instance.cliente, 'id', None)) or ''
        default_cliente_name = ''
        if default_cliente_id:
            try:
                cf_sel = Cliente.objects.filter(pk=default_cliente_id).first()
                if cf_sel:
                    default_cliente_name = (cf_sel.razon_social if getattr(cf_sel, 'razon_social', None) else (f"{getattr(cf_sel,'nombre','')} {getattr(cf_sel,'apellido','')}")).strip()
            except Exception:
                default_cliente_name = ''

        default_forma_pago_id = request.POST.get('forma_pago') or (getattr(form.instance, 'forma_pago', None) and getattr(form.instance.forma_pago, 'id', None)) or ''
        default_forma_pago_name = ''
        if default_forma_pago_id:
            try:
                fp = FormaPago.objects.filter(pk=default_forma_pago_id).first()
                if fp:
                    default_forma_pago_name = getattr(fp, 'nombre', getattr(fp, 'descripcion', str(fp)))
            except Exception:
                default_forma_pago_name = ''
        default_comentarios = request.POST.get('comentarios') or (getattr(form.instance, 'comentarios', None) or '')
        default_moneda_id = request.POST.get('moneda') or (getattr(form.instance, 'moneda', None) and getattr(form.instance.moneda, 'id', None)) or (getattr(moneda_pesos, 'id', '') if moneda_pesos else '')
        default_moneda_name = ''
        try:
            if default_moneda_id:
                m = Moneda.objects.filter(pk=default_moneda_id).first()
                if m:
                    default_moneda_name = getattr(m, 'nombre', '')
        except Exception:
            default_moneda_name = ''

        return render(request, 'ventas/venta_form.html', {
            'form': form,
            'formset': formset,
            'default_cliente_id': default_cliente_id,
            'default_cliente_name': default_cliente_name,
            'formas_pago': FormaPago.objects.all(),
            'default_forma_pago_id': default_forma_pago_id,
            'default_forma_pago_name': default_forma_pago_name,
            'default_comentarios': default_comentarios,
            'default_moneda_id': default_moneda_id,
            'default_moneda_name': default_moneda_name,
        })


def obtener_precio(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(pk=producto_id)
        precio = producto.precio
    except Producto.DoesNotExist:
        precio = 0
    return JsonResponse({'precio': precio})

def buscar_productos2(request):
    q = request.GET.get('q', '')
    if q:
        productos = Producto.objects.filter(nombre__icontains=q)
    else:
        productos = Producto.objects.all()[:50] 
    data = [{'id': p.id, 'nombre': p.nombre} for p in productos]
    return JsonResponse(data, safe=False)



class VentaDetail(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = "ventas/venta_details.html"
    context_object_name = "venta"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = (
            VentaItem.objects
            .filter(venta=self.object)
            .select_related('producto')  
        )
        for item in items:
            try:
                descuento_pct = Decimal(str(item.descuento or 0))
            except (InvalidOperation, TypeError, ValueError):
                descuento_pct = Decimal('0')

            try:
                precio = Decimal(str(item.precio)) if item.precio is not None else Decimal('0')
            except (InvalidOperation, TypeError, ValueError):
                precio = Decimal('0')
            try:
                cantidad = Decimal(str(item.cantidad)) if item.cantidad is not None else Decimal('0')
            except (InvalidOperation, TypeError, ValueError):
                cantidad = Decimal('0')

            descuento_factor = Decimal('1') - (descuento_pct / Decimal('100'))
            item.subtotal = (precio * cantidad * descuento_factor)

        total = sum((item.subtotal or Decimal('0')) for item in items)

        context.update({
            "items": items,
            "total": total,
        })

        context['venta'] = self.object

        return context


def venta_pdf_view(request, pk):
    try:
        venta = Venta.objects.get(pk=pk)
    except Venta.DoesNotExist:
        return HttpResponse("Venta no encontrada", status=404)

    items = []
    total = Decimal('0')
    for item in venta.items.all():
        precio = Decimal(str(item.precio)) if item.precio is not None else Decimal('0')
        cantidad = Decimal(str(item.cantidad)) if item.cantidad is not None else Decimal('0')
        try:
            descuento_pct = Decimal(str(item.descuento or 0))
        except Exception:
            descuento_pct = Decimal('0')
        descuento_factor = Decimal('1') - (descuento_pct / Decimal('100'))
        subtotal = (precio * cantidad * descuento_factor)
        items.append({
            'producto': item.producto.nombre if item.producto else '',
            'cantidad': item.cantidad,
            'precio': item.precio,
            'descuento': item.descuento,
            'subtotal': subtotal,
        })
        # Acumular el total de la venta (por item)
        total += subtotal

    # Recalcular por seguridad sumando todos los subtotales generados
    # (evita cualquier efecto lateral si se modifica 'total' arriba)
    try:
        total = sum((i.get('subtotal', Decimal('0')) or Decimal('0')) for i in items)
    except Exception:
        # Si algo falla, al menos conservar el acumulado previo
        pass

    import base64
    logo_path = r"productos\static\pdf\assets\img\logoFerre.png"
    logo_base64 = ''
    try:
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception:
        logo_base64 = ''

    pdf_url = request.build_absolute_uri(f'/ventas/venta/venta/{venta.id}/pdf/')
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(pdf_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    html = render_to_string('ventas/venta_pdf.html', {
        'venta': venta,
        'items': items,
        'total': total,
        'logo_base64': logo_base64,
        'qr_base64': qr_base64,
    })

    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"venta_{venta.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


def nota_credito_pdf_view(request, pk):
    try:
        from .models import NotaCredito
        nota = NotaCredito.objects.get(pk=pk)
    except Exception:
        return HttpResponse("Nota de crédito no encontrada", status=404)

    items = []
    total = Decimal('0')
    for item in nota.items.all():
        precio = Decimal(str(item.precio)) if item.precio is not None else Decimal('0')
        cantidad = Decimal(str(item.cantidad)) if item.cantidad is not None else Decimal('0')
        try:
            descuento_pct = Decimal(str(item.descuento or 0))
        except Exception:
            descuento_pct = Decimal('0')
        descuento_factor = Decimal('1') - (descuento_pct / Decimal('100'))
        subtotal = (precio * cantidad * descuento_factor)
        items.append({
            'producto': item.producto.nombre if item.producto else '',
            'cantidad': item.cantidad,
            'precio': item.precio,
            'descuento': item.descuento,
            'subtotal': subtotal,
        })
        total += subtotal

    import base64
    logo_path = r"productos\static\pdf\assets\img\logoFerre.png"
    logo_base64 = ''
    try:
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception:
        logo_base64 = ''

    pdf_url = request.build_absolute_uri(f'/ventas/notacredito/{nota.id}/pdf/')
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(pdf_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    html = render_to_string('notacredito/nota_credito_pdf.html', {
        'nota': nota,
        'items': items,
        'total': total,
        'logo_base64': logo_base64,
        'qr_base64': qr_base64,
    })

    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"nota_credito_{nota.id}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response







class VentaDelete(DeleteView):
    model = Venta
    template_name = 'ventas/venta_confirm_delete.html'
    success_url = reverse_lazy('mis_ventas')

    def delete(self, request, *args, **kwargs):
        venta = self.get_object()
        try:
            logging.getLogger(__name__).debug("VentaDelete.delete called for venta id=%s user=%s", venta.pk, request.user)
        except Exception:
            pass

        debug_requested = (
            request.user.is_staff or
            request.GET.get('debug') == '1' or
            request.POST.get('debug') == '1' or
            request.headers.get('x-requested-with') == 'XMLHttpRequest'
        )

        if getattr(venta, 'anulada', False):
            logging.getLogger(__name__).info("VentaDelete: venta %s ya está anulada; no se permite eliminar.", getattr(venta, 'pk', None))
            if debug_requested:
                return JsonResponse({'deleted': False, 'reason': 'anulada', 'venta_id': venta.pk})
            messages.info(request, "La venta ya está anulada y no se puede eliminar.")
            return redirect(self.get_success_url())

        nota = None
        applied_count = 0
        error_msg = None
        pre_items = list(venta.items.select_related('producto').values('id', 'producto_id', 'cantidad', 'stock_aplicado'))

        try:
            from .models import create_nota_from_venta, apply_stock_for_nota, NotaCredito
            from django.db import transaction

            logger = logging.getLogger(__name__)
            logger.info("Starting atomic delete flow for venta %s", getattr(venta, 'pk', None))
            try:
                with transaction.atomic():
                    nota = create_nota_from_venta(venta)
                    logger.info("create_nota_from_venta returned: %s", getattr(nota, 'pk', None))

                    if nota is None or not NotaCredito.objects.filter(pk=getattr(nota, 'pk', None)).exists():
                        raise Exception("La nota de crédito no se llegó a crear en la base de datos.")

                    applied_count = apply_stock_for_nota(nota)

                    venta.anulada = True
                    venta.save(update_fields=['anulada'])

            except Exception:
                logging.getLogger(__name__).exception("Error during atomic create/apply/anular for venta %s", getattr(venta, 'pk', None))
                raise
        except Exception as e:
            try:
                logging.getLogger(__name__).exception("Error creando/aplicando nota de credito para venta %s: %s", getattr(venta, 'pk', None), str(e))
            except Exception:
                pass
            error_msg = str(e)

        if error_msg:
            messages.error(request, f"Ocurrió un error creando/aplicando la nota de crédito: {error_msg}")
        else:
            messages.success(request, "La venta fue eliminada y la nota de crédito procesada correctamente.")
        nota_items = []
        if nota is not None:
            nota_items = list(nota.items.select_related('producto').values('id', 'producto_id', 'cantidad', 'stock_aplicado'))

        debug_requested = (
            request.user.is_staff or
            request.GET.get('debug') == '1' or
            request.POST.get('debug') == '1' or
            request.headers.get('x-requested-with') == 'XMLHttpRequest'
        )
        if debug_requested:
            return JsonResponse({
                'deleted': True,
                'venta_id': venta.pk,
                'nota_id': getattr(nota, 'pk', None),
                'applied_count': applied_count,
                'nota_items': nota_items,
                'pre_items': pre_items,
                'error': error_msg,
            })

        try:
            venta.anulada = True
            venta.save(update_fields=['anulada'])
        except Exception:
            try:
                logging.getLogger(__name__).exception("No se pudo marcar venta %s como anulada", getattr(venta, 'pk', None))
            except Exception:
                pass

        try:
            from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
            base = str(self.get_success_url())
            scheme, netloc, path, query, frag = urlsplit(base)
            q = dict(parse_qsl(query))
            if nota is not None:
                q['nota_id'] = str(nota.pk)
            q['applied'] = str(applied_count)
            new_query = urlencode(q)
            new_loc = urlunsplit((scheme, netloc, path, new_query, frag))
            return redirect(new_loc)
        except Exception:
            return redirect(self.get_success_url())
