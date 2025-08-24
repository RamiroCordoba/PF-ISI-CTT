from django import forms
from .models import *
from django_select2.forms import Select2Widget
from django.forms import inlineformset_factory

#_______ Formulario de proveedor
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "razon_social", "email", "cuit", "telefono", "direccion", "condicion_fiscal"]
        widgets = {
            'condicion_fiscal': Select2Widget,
        }


class IVAForm(forms.ModelForm):
    class Meta:
        model = Iva
        fields = ["nombre", "porcentaje", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "porcentaje": forms.NumberInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = ['nombre', 'simbolo', 'activo']
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "simbolo": forms.TextInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }
class CondicionFiscalForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = ['nombre', 'activo']
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }
