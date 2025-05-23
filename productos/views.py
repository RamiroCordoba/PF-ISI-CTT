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
#______ Productos