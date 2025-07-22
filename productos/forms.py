from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombreEmpresa", "nombreProv", "telefono", "mail", "estado", "direccion", "provincia", "ciudad", "categoria"]
        widgets = {
            'categoria': forms.CheckboxSelectMultiple()
        }
