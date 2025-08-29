from django import forms
from .models import Proveedor,Producto,Pedido,PedidoItem
import datetime
from django.forms import inlineformset_factory

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
    fecha_registro_display = forms.DateTimeField(
        label='Fecha de registro',
        required=False,
        disabled=True,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        }, format='%Y-%m-%d %H:%M:%S')
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'stock_optimo', 'stock_minimo', 'stock_maximo',
                  'categoria', 'marca', 'proveedores', 'activo', 'fecha_ultimo_ingreso']
        widgets = {
            'proveedores': forms.CheckboxSelectMultiple,
            'fecha_ultimo_ingreso': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Fecha',
                },
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fecha_registro_display'].initial = self.instance.fecha_registro

    def clean_fecha_ultimo_ingreso(self):
        fecha = self.cleaned_data.get('fecha_ultimo_ingreso')
        if fecha:
            # Convertir a datetime con hora 00:00:00
            return datetime.datetime.combine(fecha, datetime.time.min)
        return fecha


#_______ Carga masiva de productos

class CargaMasivaProductosForm(forms.Form):
    archivo_excel = forms.FileField(label="Archivo Excel (.xlsx)")

    def clean_archivo_excel(self):
        archivo = self.cleaned_data['archivo_excel']
        if not archivo.name.endswith('.xlsx'):
            raise forms.ValidationError("El archivo debe tener extensión .xlsx")
        return archivo
    

#_______ Pedidos

class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ['producto', 'cantidad', 'precio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].empty_label = ''
        # Valores iniciales por defecto
        self.fields['cantidad'].initial = 1
        self.fields['precio'].initial = 0.00


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'proveedor',
            'comentarios',
            'completado',
            'fechaIngreso',
            'forma_pago',
            'fechaEstimadaEntrega'
        ]
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 3}),
            'fechaIngreso': forms.DateInput(attrs={'type': 'date'}),
            'fechaEstimadaEntrega': forms.DateInput(attrs={'type': 'date'},
            format='%Y-%m-%d'),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance and self.instance.pk):
            try:
                self.fields['fechaEstimadaEntrega'].initial = datetime.date.today() + datetime.timedelta(days=7)
            except Exception:
                pass

        if self.instance and self.instance.pk:
            self.fields['completado'].label = '¿Completado?'
            self.fields['fechaIngreso'].label = 'Fecha de ingreso'
            self.fields['proveedor'].disabled = True
        self.fields['fechaEstimadaEntrega'].label = 'Fecha estimada entrega'


    def clean(self):
        cleaned_data = super().clean()
        completado = cleaned_data.get('completado')
        fecha_ingreso = cleaned_data.get('fechaIngreso')

        if completado and not fecha_ingreso:
            self.add_error('fechaIngreso', 'Debe ingresar la fecha de ingreso al completar el pedido.')
        if self.instance and self.instance.pk and self.instance.completado:
            cleaned_data['completado'] = True
        if self.instance.pk:
            proveedor_enviado = cleaned_data.get('proveedor')
            if proveedor_enviado != self.instance.proveedor:
                self.add_error('proveedor', 'No se puede modificar el proveedor de un pedido ya creado.')



# PedidoItemFormSet para crear (con fila vacía)
PedidoItemFormSet = inlineformset_factory(
    Pedido,
    PedidoItem,
    form=PedidoItemForm,
    extra=1,
    can_delete=True
)

# PedidoItemFormSet para editar (sin fila vacía extra)
PedidoItemFormSetNoExtra = inlineformset_factory(
    Pedido,
    PedidoItem,
    form=PedidoItemForm,
    extra=0,
    can_delete=True
)
