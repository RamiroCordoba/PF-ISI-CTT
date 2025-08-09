from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProveedorForm, CargaMasivaProductosForm, ProductoForm
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
from django.utils.timezone import now
from datetime import datetime
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
    paginate_by = 50  # Display 50 articles per page

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

        # Pagination logic
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
        context["articulos"] = articulos_paginated.object_list  # Paginated articles

        # Add categories and providers for filters
        context["categorias"] = Categoria.objects.all()
        context["proveedores"] = Proveedor.objects.all()

        # Active filters
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

class ArticuloUpdate(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "articulos/articulo_form.html"
    success_url = reverse_lazy("mis_articulos")

class ArticuloDelete(LoginRequiredMixin,DeleteView):
     model=Producto
     template_name="articulos/articulo_confirm_delete.html"
     success_url = reverse_lazy("mis_articulos")

class ArticuloDetail(DetailView):
     model=Producto
     template_name="articulos/articulo_details.html"
     context_object_name = 'elArticulo'

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
                    precio = float(fila['precio'])
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

class ProveedorList(LoginRequiredMixin,ListView):
    model = Proveedor
    template_name = "proveedores/proveedor_list.html"
    context_object_name = "proveedores"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")
        buscar = self.request.GET.get("buscar")
        #proveedor_id = self.request.GET.get("proveedor")

        if buscar:
            queryset = queryset.filter(nombreEmpresa__icontains=buscar)

        #if proveedor_id:
        #    queryset = queryset.filter(proveedor_id=proveedor_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["proveedores"] = Proveedor.objects.all().order_by("nombreEmpresa")
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
        #estacionalidad_id = self.request.GET.get("estacionalidad")

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        #if estacionalidad_id:
        #    queryset = queryset.filter(estacionalidad_id=estacionalidad_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["estacionalidades"] = Estacionalidad.objects.all().order_by("nombre")
        return context
