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


  
class ClienteCreate(LoginRequiredMixin,CreateView):
     model=Cliente
     form_class = ClienteForm
     #fields = ['nombre', 'apellido', 'razon_social', 'email', 'cuit', 'telefono', 'direccion', 'condicion_fiscal']
     template_name="cliente/cliente_form.html"
     success_url = reverse_lazy("mis_clientes")
     
class ClienteUpdate(LoginRequiredMixin,UpdateView):
     model=Cliente
     form_class = ClienteForm
     #fields = ['nombre', 'apellido', 'razon_social', 'email', 'cuit', 'telefono', 'direccion', 'condicion_fiscal']
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

def autocomplete_productos2(request):
    term = request.GET.get("term", "")
    proveedor_id = request.GET.get("proveedor_id")

    productos = Producto.objects.filter(nombre__icontains=term)

    if proveedor_id:  # solo filtrar por proveedor si hay valor
        productos = productos.filter(proveedores__id=proveedor_id)

    # Limitar a máximo 20 resultados
    productos = productos[:20]

    results = [
        {
            "id": p.id,
            "value": p.nombre,        # <-- Esto se muestra en el input
            "precio": float(p.precio) if p.precio else 0
        } 
        for p in productos
    ]
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

class VentaCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = VentaForm()
        formset = VentaItemFormSet()
        return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

    def post(self, request):
        form = VentaForm(request.POST)
        formset = VentaItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            items = formset.save(commit=False)
            items_validos = [item for item in items if item.producto and item.cantidad]

            if not items_validos:
                formset._non_form_errors = formset.error_class([
                    "Debe agregar al menos un producto con cantidad."
                ])
    
                return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

            venta = form.save()

            for item in items_validos:
                item.venta = venta
                item.save()

            if venta.completado:
                for item in items_validos:
                    producto = item.producto
                    producto.stock += item.cantidad
                    producto.save()
                messages.success(request, "Venta confirmada y stock actualizado.")
            else:
                messages.success(request, "Venta guardada correctamente.")

            return redirect('listar_Ventas')

        return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})


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
            item.subtotal = (item.precio or 0) * (item.cantidad or 0)

        # Total general
        total = sum(item.subtotal for item in items)

        context.update({
            "items": items,
            "total": total,
        })

        return context




class VentaUpdate(LoginRequiredMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object.completado:
            for field in form.fields.values():
                field.disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = self.object

        if self.request.POST:
            formset = VentaItemFormSet(self.request.POST, instance=venta)
        else:
            VentaItemFormSetNoExtra = inlineformset_factory(
                Venta,
                VentaItem,
                fields=["producto", "cantidad", "precio"],
                extra=0,
                can_delete=True
            )
            formset = VentaItemFormSetNoExtra(instance=venta)

            if venta.completado:
                for form in formset.forms:
                    for field in form.fields.values():
                        field.disabled = True

        context["formset"] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        venta_original = Venta.objects.get(pk=self.object.pk)
        estaba_completado = venta_original.completado

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            # Actualizar stock solo si se marca como completado ahora
            if self.object.completado and not estaba_completado:
                for item in self.object.items.all():
                    producto = item.producto
                    producto.stock += item.cantidad
                    producto.save()

            mensaje = (
                "El pedido fue confirmado y el stock actualizado."
                if self.object.completado
                else "El pedido fue guardado correctamente."
            )
            messages.success(self.request, mensaje)

            return redirect("mis_ventas")

        return self.render_to_response(self.get_context_data(form=form))



class VentaDelete(DeleteView):
    model = Venta
    template_name = 'ventas/venta_confirm_delete.html'
    success_url = reverse_lazy('mis_ventas')

    def delete(self, request, *args, **kwargs):
        venta = self.get_object()

        if venta.completado:
            messages.warning(request, "No se puede eliminar una venta ya confirmada.")
            return redirect(self.success_url)

        messages.success(request, "La venta fue eliminada correctamente.")
        return super().delete(request, *args, **kwargs)
