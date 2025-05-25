from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import *

#______ Categorias CRUD
class CategoriaList(ListView):
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
  
class CategoriaCreate(CreateView):
     model=Categoria
     fields=["nombre","descripcion"]
     template_name="categorias/categoria_form.html"
     success_url = reverse_lazy("categorias")
     
class CategoriaUpdate(UpdateView):
     model=Categoria
     fields=["nombre","descripcion"]
     template_name="categorias/categoria_form.html"
     success_url = reverse_lazy("categorias")

class CategoriaDelete(DeleteView):
     model=Categoria
     template_name="categorias/categoria_confirm_delete.html"
     success_url = reverse_lazy("categorias")

#______ Productos CRUD

class ProductoList(ListView):
    model = Producto
    template_name = "productos/producto_list.html"
    context_object_name = "productos"

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
        from .models import Categoria
        context["categorias"] = Categoria.objects.all().order_by("nombre")
        return context

  
class ProductoCreate(CreateView):
     model=Producto
     fields=["nombre","descripcion","precio","stock","stock_maximo","stock_minimo","categoria","marca","fecha_ultimo_ingreso","activo"]
     template_name="productos/producto_form.html"
     success_url = reverse_lazy("misproductos")
     
class ProductoUpdate(UpdateView):
     model=Producto
     fields=["nombre","descripcion","precio","stock","stock_maximo","stock_minimo","categoria","marca","fecha_ultimo_ingreso","activo"]
     template_name="productos/producto_form.html"
     success_url = reverse_lazy("misproductos")

class ProductoDelete(DeleteView):
     model=Producto
     template_name="productos/producto_confirm_delete.html"
     success_url = reverse_lazy("misproductos")
