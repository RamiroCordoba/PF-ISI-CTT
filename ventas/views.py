from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy

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
