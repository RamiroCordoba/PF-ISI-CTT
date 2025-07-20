from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProveedorForm
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

class ArticuloList(LoginRequiredMixin,ListView):
    model = Producto
    template_name = "articulos/articulo_list.html"
    context_object_name = "articulos"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")
        buscar = self.request.GET.get("buscar")
        categoria_id = self.request.GET.get("categoria")

        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all().order_by("nombre")
        return context

  
class ArticuloCreate(LoginRequiredMixin,CreateView):
     model=Producto
     fields=["nombre","descripcion","precio","stock","stock_maximo","stock_minimo","stock_optimo","categoria","marca","fecha_ultimo_ingreso","activo"]
     template_name="articulos/articulo_form.html"
     success_url = reverse_lazy("mis_articulos")
     
class ArticuloUpdate(LoginRequiredMixin,UpdateView):
     model=Producto
     fields=["nombre","descripcion","precio","stock","stock_maximo","stock_minimo","stock_optimo","categoria","marca","fecha_ultimo_ingreso","activo"]
     template_name="articulos/articulo_form.html"
     success_url = reverse_lazy("mis_articulos")

class ArticuloDelete(LoginRequiredMixin,DeleteView):
     model=Producto
     template_name="articulos/articulo_confirm_delete.html"
     success_url = reverse_lazy("mis_articulos")

class ArticuloDetail(DetailView):
     model=Producto
     template_name="articulos/articulo_details.html"
     context_object_name = 'elArticulo'

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

#Estacionalidad
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
