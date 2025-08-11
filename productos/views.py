from django.shortcuts import render, redirect ,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProveedorForm, CargaMasivaProductosForm, ProductoForm,PedidoForm, PedidoItemFormSet,inlineformset_factory

from django.views import View
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
from django.utils.timezone import now
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#______ Categorias CRUD
class CategoriaList(LoginRequiredMixin, ListView):
  model=Categoria
  template_name="categorias/categoria_list.html"
  context_object_name="categorias"
  queryset = Categoria.objects.all().order_by("id")
  
  def get_queryset(self):
          queryset = super().get_queryset().order_by("id")
          buscar = self.request.GET.get("buscar")

          if buscar:
              queryset = queryset.filter(nombre__icontains=buscar)
          
          return queryset

class CategoriaCreate(LoginRequiredMixin,CreateView):
     model=Categoria
     fields=["nombre","descripcion"]
     template_name="categorias/categoria_form.html"
     success_url = reverse_lazy("categorias")
     
class CategoriaUpdate(LoginRequiredMixin,UpdateView):
     model=Categoria
     fields=["nombre","descripcion"]
     template_name="categorias/categoria_form.html"
     success_url = reverse_lazy("categorias")

class CategoriaDelete(LoginRequiredMixin,DeleteView):
     model=Categoria
     template_name="categorias/categoria_confirm_delete.html"
     success_url = reverse_lazy("categorias")

#______ Productos CRUD
class ArticuloList(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "articulos/articulo_list.html"
    context_object_name = "articulos"
    paginate_by = 25  

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")
        buscar = self.request.GET.get("buscar")
        categoria_ids = self.request.GET.getlist("categoria")
        proveedor_ids = self.request.GET.getlist("proveedor")
        estados = self.request.GET.getlist("estado")

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        if categoria_ids:
            queryset = queryset.filter(categoria_id__in=categoria_ids)

        if proveedor_ids:
            queryset = queryset.filter(proveedores__id__in=proveedor_ids)

        if "activos" in estados and "inactivos" not in estados:
            queryset = queryset.filter(activo=True)
        elif "inactivos" in estados and "activos" not in estados:
            queryset = queryset.filter(activo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        # Paginacion de articulos
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('page')

        try:
            articulos_paginated = paginator.page(page)
        except PageNotAnInteger:
            articulos_paginated = paginator.page(1)
        except EmptyPage:
            articulos_paginated = paginator.page(paginator.num_pages)

        context["page_obj"] = articulos_paginated
        context["articulos"] = articulos_paginated.object_list 

        # Filtros
        context["categorias"] = Categoria.objects.all()
        context["proveedores"] = Proveedor.objects.all()

        context["filtro_estados"] = request.GET.getlist("estado")
        context["filtro_categorias"] = request.GET.getlist("categoria")
        context["filtro_proveedores"] = request.GET.getlist("proveedor")
        context["filtros_activos"] = (
            bool(context["filtro_estados"])
            or bool(context["filtro_categorias"])
            or bool(context["filtro_proveedores"])
        )
        return context


class ArticuloCreate(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "articulos/articulo_form.html"
    success_url = reverse_lazy("mis_articulos")

    def form_valid(self, form):
        estado = self.request.POST.get('estado', 'True')
        form.instance.activo = True if estado == 'True' else False
        return super().form_valid(form)

class ArticuloUpdate(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "articulos/articulo_form.html"
    success_url = reverse_lazy("mis_articulos")

    def form_valid(self, form):
        estado = self.request.POST.get('estado', 'True')
        form.instance.activo = True if estado == 'True' else False
        return super().form_valid(form)

class ArticuloDelete(LoginRequiredMixin,DeleteView):
     model=Producto
     template_name="articulos/articulo_confirm_delete.html"
     success_url = reverse_lazy("mis_articulos")

class ArticuloDetail(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = "articulos/articulo_details.html"
    context_object_name = 'elArticulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todos_proveedores"] = Proveedor.objects.exclude(id__in=self.object.proveedores.all())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        proveedor_id = request.POST.get("proveedor_id")
        if proveedor_id:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            self.object.proveedores.add(proveedor)
            messages.success(request, "Proveedor agregado correctamente.")
        quitar_id = request.POST.get("quitar_proveedor_id")
        if quitar_id:
            proveedor = Proveedor.objects.get(id=quitar_id)
            self.object.proveedores.remove(proveedor)
            messages.success(request, "Proveedor quitado correctamente.")
        return redirect(f"{reverse('detalles_de_articulo', args=[self.object.pk])}#proveedores")

@login_required
def proveedores_grilla(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    proveedores = producto.proveedores.all()
    todos_proveedores = Proveedor.objects.exclude(id__in=proveedores)

    if request.method == "POST":
        proveedor_id = request.POST.get("proveedor_id")
        if proveedor_id:
            proveedor = get_object_or_404(Proveedor, id=proveedor_id)
            producto.proveedores.add(proveedor)
            messages.success(request, "Proveedor agregado correctamente.")
            return redirect('proveedores_grilla', pk=pk)

    return render(request, "articulos/proveedores_grilla.html", {
        "producto": producto,
        "proveedores": proveedores,
        "todos_proveedores": todos_proveedores,
    })

@login_required
def quitar_proveedor(request, pk, proveedor_id):
    producto = get_object_or_404(Producto, pk=pk)
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    producto.proveedores.remove(proveedor)
    messages.success(request, "Proveedor quitado correctamente.")
    return redirect('proveedores_grilla', pk=pk)


class CargaMasivaProductosView(View):
    template_name = 'articulos/carga_masiva_productos.html'

    def get(self, request):
        form = CargaMasivaProductosForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CargaMasivaProductosForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_excel']

            # Validar extensión del archivo
            if not archivo.name.endswith('.xlsx'):
                messages.error(request, "El archivo debe tener extensión .xlsx   ")
                return redirect('carga_masiva_productos')

            try:
                df = pd.read_excel(archivo, dtype={'proveedores': 'string'})
            except Exception as e:
                messages.error(request, f"Error al leer el archivo: {str(e)}")
                return redirect('carga_masiva_productos')

            errores = []
            productos_agregados = []
            productos_actualizados = []
            proveedores_actualizados = []
            proveedores_no_existentes = []
            for index, fila in df.iterrows():
                # Saltar fila vacía completa
                if fila.isnull().all():
                    continue

                try:
                    nombre = str(fila['nombre']).strip()
                    if not nombre:
                        raise ValueError("El campo 'nombre' está vacío")

                    descripcion = str(fila.get('descripcion', '')).strip()
                    precio = float(str(fila['precio']).replace(',', '.'))
                    stock = int(fila['stock'])
                    stock_optimo = int(fila['stock_optimo'])
                    stock_maximo = int(fila.get('stock_maximo')) if not pd.isna(fila.get('stock_maximo')) else None
                    stock_minimo = int(fila.get('stock_minimo')) if not pd.isna(fila.get('stock_minimo')) else None
                    marca = str(fila.get('marca', '')).strip()
                    activo = True
                    categoria_nombre = str(fila['categoria']).strip()
                    categoria_obj = Categoria.objects.filter(nombre__iexact=categoria_nombre).first()
                    if not categoria_obj:
                        raise ValueError(f"Categoría '{categoria_nombre}' no encontrada")
                    

                    producto, creado = Producto.objects.get_or_create(nombre=nombre, defaults={
                        'descripcion': descripcion,
                        'precio': precio,
                        'stock': stock,
                        'stock_optimo': stock_optimo,
                        'stock_maximo': stock_maximo,
                        'stock_minimo': stock_minimo,
                        'categoria': categoria_obj,
                        'activo': activo,
                        'marca': marca,
                        'fecha_ultimo_ingreso': now(),
                    })
                    
                    raw_proveedor = fila.get('proveedores', None)
                    if pd.isna(raw_proveedor):
                        proveedor_nombre = ''
                    else:
                        proveedor_nombre = str(raw_proveedor).strip()

                    if proveedor_nombre.lower() == 'nan':
                        proveedor_nombre = ''

                    if proveedor_nombre:
                        proveedor_obj = Proveedor.objects.filter(nombreEmpresa__iexact=proveedor_nombre).first()
                        if not proveedor_obj:
                            proveedor_obj = None  
                    else:
                        proveedor_obj = None  
                    if creado:
                        if proveedor_obj:
                            producto.proveedores.set([proveedor_obj])
                        else:
                            producto.proveedores.clear()

                    if not creado:
                        cambios = False
                        datos = {
                            'descripcion': descripcion,
                            'precio': precio,
                            'stock': stock,
                            'stock_optimo': stock_optimo,
                            'stock_maximo': stock_maximo,
                            'stock_minimo': stock_minimo,
                            'categoria': categoria_obj,
                            'activo': activo,
                            'marca': marca,
                        }

                        for campo, valor_nuevo in datos.items():
                            if getattr(producto, campo) != valor_nuevo:
                                setattr(producto, campo, valor_nuevo)
                                cambios = True
                        if proveedor_nombre:
                            if proveedor_obj:
                                if not producto.proveedores.filter(pk=proveedor_obj.pk).exists():
                                    producto.proveedores.add(proveedor_obj)
                                    cambios = True
                                    proveedores_actualizados.append(
                                        f"{nombre} (proveedor agregado: {proveedor_obj.nombreEmpresa})"
                                    )
                            else:
                                proveedores_no_existentes.append(f"{nombre} (proveedor: {proveedor_nombre})")
                        else:
                            if producto.proveedores.exists():
                                producto.proveedores.clear()
                                cambios = True
                                proveedores_actualizados.append(f"{nombre} (proveedores eliminados)")

                        if cambios:
                            producto.fecha_ultimo_ingreso = now()
                            producto.save()
                            productos_actualizados.append(nombre)
                    else:
                        productos_agregados.append(nombre)

                except Exception as e:
                    errores.append(f"Fila {index + 2} - Error: {str(e)}")

            if errores:
                for error in errores:
                    messages.error(request, error)
            def label(base_singular, base_plural, n):
                return base_singular if n == 1 else base_plural
            if productos_agregados:
                n = len(productos_agregados)
                messages.success(
                    request,
                    f"{n} {label('producto agregado', 'productos agregados', n)}: {', '.join(productos_agregados)}"
                )

            if productos_actualizados:
                n = len(productos_actualizados)
                messages.info(
                    request,
                    f"{n} {label('producto actualizado', 'productos actualizados', n)}: {', '.join(productos_actualizados)}"
                )
            if proveedores_actualizados:
                n = len(proveedores_actualizados)
                messages.info(
                    request,
                    f"{n} {label('proveedor actualizado', 'proveedores actualizados', n)}: {', '.join(proveedores_actualizados)}"
                )

            if proveedores_no_existentes:
                n = len(proveedores_no_existentes)
                messages.warning(
                    request,
                    f"{n} {label('proveedor inexistente', 'proveedores inexistentes', n)}: {', '.join(proveedores_no_existentes)}"
                )
            if not productos_agregados and not productos_actualizados and not errores:
                messages.info(request, "No se detectaron cambios.")

            return redirect('carga_masiva_productos')

        return render(request, self.template_name, {'form': form})

#_____ Descarga del archivo

class ExportarProductosExcelView(View):
    def get(self, request):
        productos = Producto.objects.all().select_related('categoria')
        data = []

        for p in productos:
            prov_nombres = list(p.proveedores.values_list('nombreEmpresa', flat=True))
            prov_str = ', '.join(prov_nombres) if prov_nombres else '' 
            data.append({
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'precio': float(p.precio),
                'stock': p.stock,
                'stock_optimo': p.stock_optimo,
                'stock_maximo': p.stock_maximo,
                'stock_minimo': p.stock_minimo,
                'categoria': p.categoria.nombre,
                'marca': p.marca or '',
                'proveedores': prov_str
            })

        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime('%d_%m_%Y_%H_%Mhs') # Obtengo los datos de fecha y hora/min
        filename = f'listado_productos_{timestamp}.xlsx'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        df.to_excel(response, index=False, engine='openpyxl')
        return response

#______ Productos CRUD
class ProveedorCreate(LoginRequiredMixin,CreateView):
     model=Proveedor
     fields=["nombreEmpresa","nombreProv","telefono","mail","estado","direccion","provincia","ciudad","categoria"]
     template_name="proveedores/proveedor_form.html"
     success_url = reverse_lazy("mis_proveedores") 

class ProveedorUpdate(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/proveedor_form.html"
    success_url = reverse_lazy("mis_proveedores")

class ProveedorDelete(LoginRequiredMixin,DeleteView):
     model=Proveedor
     template_name="proveedores/proveedor_confirm_delete.html"
     success_url = reverse_lazy("mis_proveedores")

class ProveedorDetail(DetailView):
     model=Proveedor
     template_name="proveedores/proveedor_details.html"
     context_object_name = 'elProveedor'


class ProveedorList(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = "proveedores/proveedor_list.html"
    context_object_name = "proveedores"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")
        request = self.request

        # Filtro por empresa
        empresa = request.GET.get('empresa', '').strip()
        if empresa:
            queryset = queryset.filter(nombreEmpresa__icontains=empresa)

        # Filtro por categoría (ManyToMany)
        categorias = request.GET.getlist('categoria')
        if categorias:
            queryset = queryset.filter(categoria__id__in=categorias)

        # Filtro por estado
        estado = request.GET.get('estado')
        if estado == 'activos':
            queryset = queryset.filter(estado=True)
        elif estado == 'inactivos':
            queryset = queryset.filter(estado=False)

        # Buscador por texto
        buscar = request.GET.get('buscar', '').strip()
        buscar = self.request.GET.get("buscar")

        if buscar:
            queryset = queryset.filter(
                models.Q(nombreEmpresa__icontains=buscar) |
                models.Q(nombreProv__icontains=buscar) |
                models.Q(mail__icontains=buscar) |
                models.Q(ciudad__icontains=buscar)
            )

        queryset = queryset.distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context['empresas'] = Proveedor.objects.values_list('nombreEmpresa', flat=True).distinct().order_by('nombreEmpresa')
        context['categorias'] = Categoria.objects.all()
        context['filtro_empresa'] = request.GET.get('empresa', '')
        context['filtro_categorias'] = request.GET.getlist('categoria')
        context['filtro_estado'] = request.GET.get('estado', '')
        context['buscar'] = request.GET.get('buscar', '')
        context['filtros_activos'] = bool(context['filtro_empresa'] or context['filtro_categorias'] or context['filtro_estado'] or context['buscar'])
        return context

#______ Estacionalidad
class EstacionalidadCreate(LoginRequiredMixin,CreateView):
     model=Estacionalidad
     fields=["producto","nombre","estacion","diaDesde","mesDesde","diaHasta","mesHasta","stockMin","stockMax"]
     template_name="estacionalidades/estacionalidad_form.html"
     success_url = reverse_lazy("mis_estacionalidades")
     
class EstacionalidadUpdate(LoginRequiredMixin,UpdateView):
     model=Estacionalidad
     fields=["producto","nombre","estacion","diaDesde","mesDesde","diaHasta","mesHasta","stockMin","stockMax"]
     template_name="estacionalidades/estacionalidad_form.html"
     success_url = reverse_lazy("mis_estacionalidades")

class EstacionalidadDelete(LoginRequiredMixin,DeleteView):
     model=Estacionalidad
     template_name="estacionalidades/estacionalidad_confirm_delete.html"
     success_url = reverse_lazy("mis_estacionalidades")

class EstacionalidadDetail(DetailView):
     model=Estacionalidad
     template_name="estacionalidades/estacionalidad_details.html"
     context_object_name = 'laEstacionalidad'

class EstacionalidadList(LoginRequiredMixin,ListView):
    model = Estacionalidad
    template_name = "estacionalidades/estacionalidad_list.html"
    context_object_name = "estacionalidades"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")
        buscar = self.request.GET.get("buscar")

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PedidoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PedidoForm()
        formset = PedidoItemFormSet()
        return render(request, 'pedidos/pedido_form.html', {'form': form, 'formset': formset})

    def post(self, request):
        form = PedidoForm(request.POST)
        formset = PedidoItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.pedido = pedido
                item.save()
            return redirect('listar_pedidos')
        return render(request, 'pedidos/pedido_form.html', {'form': form, 'formset': formset})

"""def listar_pedidos(request):
    pedidos = Pedido.objects.select_related('proveedor').all().order_by('-fecha')
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})"""


class PedidosList(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 10  

    def get_queryset(self):
        qs = super().get_queryset().select_related('proveedor')
        request = self.request
        filtro_estados = request.GET.getlist('estado')
        filtro_proveedores = request.GET.getlist('proveedor')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        buscar = request.GET.get('buscar')

        if filtro_estados:
            if "completado" in filtro_estados:
                qs = qs.filter(completado=True)
            if "pendiente" in filtro_estados:
                qs = qs.filter(completado=False)

        if filtro_proveedores:
            qs = qs.filter(proveedor__id__in=filtro_proveedores)

        if fecha_inicio:
            qs = qs.filter(fecha__gte=fecha_inicio)

        if fecha_fin:
            qs = qs.filter(fecha__lte=fecha_fin)

        if buscar:
            qs = qs.filter(comentarios__icontains=buscar)

        return qs.order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        context['proveedores'] = Proveedor.objects.all()  
        context['filtro_estados'] = request.GET.getlist('estado')
        context['filtro_proveedores'] = request.GET.getlist('proveedor')
        context['filtros_activos'] = bool(
            context['filtro_estados'] or context['filtro_proveedores'] or
            request.GET.get('fecha_inicio') or request.GET.get('fecha_fin') or
            request.GET.get('buscar')
        )
        context['request'] = request 

        return context



def autocomplete_productos(request):
    term = request.GET.get('term', '')
    proveedor_id = request.GET.get('proveedor_id')
    productos = Producto.objects.all()
    if proveedor_id:
        productos = productos.filter(proveedores__id=proveedor_id)
    if term:
        productos = productos.filter(nombre__icontains=term)
    productos = productos[:10]
    results = []
    for producto in productos:
        results.append({'id': producto.id, 'label': producto.nombre, 'value': producto.nombre})
    return JsonResponse(results, safe=False)

def productos_por_proveedor(request):
    proveedor_id = request.GET.get('proveedor_id')
    productos = []
    if proveedor_id:
        productos_qs = Producto.objects.filter(proveedores__id=proveedor_id)
        productos = list(productos_qs.values('id', 'nombre'))
    return JsonResponse({'productos': productos})

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = "pedidos/pedido_details.html"
    context_object_name = "pedido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = PedidoItem.objects.filter(pedido=self.object)
        for item in items:
            item.subtotal = (item.precio or 0) * item.cantidad

        context["items"] = items
        context["total"] = sum(item.subtotal for item in items)
        return context



class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/pedido_form.html"

    """def dispatch(self, request, *args, **kwargs):
        pedido = self.get_object()
        if pedido.completado:
            messages.warning(request, "Este pedido ya fue confirmado y no puede editarse.")
            return redirect("listar_pedidos")
        return super().dispatch(request, *args, **kwargs)"""
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.get_object().completado:
            for field in form.fields.values():
                field.disabled = True
        return form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido = self.object
        
        if self.request.POST:
            formset = PedidoItemFormSet(self.request.POST, instance=pedido)
        else:
            PedidoItemFormSetNoExtra = inlineformset_factory(
                Pedido,
                PedidoItem,
                fields=["producto", "cantidad", "precio"],
                extra=0,
                can_delete=True
            )
            formset = PedidoItemFormSetNoExtra(instance=pedido)

            if pedido.completado:
                for form in formset.forms:
                    for field in form.fields.values():
                        field.disabled = True

        context["formset"] = formset
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            if self.object.completado:
                messages.success(self.request, "El pedido fue confirmado correctamente.")
            else:
                messages.success(self.request, "El pedido fue guardado correctamente.")

            return redirect("listar_pedidos")
        else:
            return self.render_to_response(self.get_context_data(form=form))




class PedidoDelete(DeleteView):
    model = Pedido
    template_name = 'pedidos/pedido_confirm_delete.html'
    success_url = reverse_lazy('listar_pedidos')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Pedido eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
