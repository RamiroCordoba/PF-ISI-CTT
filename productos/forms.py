from django import forms
from .models import Proveedor

#_______ Formulario de proveedor
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombreEmpresa", "nombreProv", "telefono", "mail", "estado", "direccion", "provincia", "ciudad", "categoria"]
        widgets = {
            'categoria': forms.CheckboxSelectMultiple()
        }

#_______ Carga masiva de productos

class CargaMasivaProductosForm(forms.Form):
    archivo_excel = forms.FileField(label="Archivo Excel (.xlsx)")

    def clean_archivo_excel(self):
        archivo = self.cleaned_data['archivo_excel']
        if not archivo.name.endswith('.xlsx'):
            raise forms.ValidationError("El archivo debe tener extensión .xlsx")
        return archivo

