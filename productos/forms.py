from django import forms
from .models import Proveedor,Producto

#_______ Formulario de proveedor
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombreEmpresa", "nombreProv", "telefono", "mail", "estado", "direccion", "provincia", "ciudad", "categoria"]
        widgets = {
            'categoria': forms.CheckboxSelectMultiple()
        }

#_______ Formulario de producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock','stock_optimo', 'stock_minimo', 'stock_maximo','categoria', 'marca', 'proveedores', 'activo']
        widgets = {'proveedores': forms.CheckboxSelectMultiple,}

#_______ Carga masiva de productos

class CargaMasivaProductosForm(forms.Form):
    archivo_excel = forms.FileField(label="Archivo Excel (.xlsx)")

    def clean_archivo_excel(self):
        archivo = self.cleaned_data['archivo_excel']
        if not archivo.name.endswith('.xlsx'):
            raise forms.ValidationError("El archivo debe tener extensión .xlsx")
        return archivo

