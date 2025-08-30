from django import forms
from .models import *
from django_select2.forms import Select2Widget
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

#_______ Formulario de proveedor
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



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'razon_social', 'email', 'cuit', 'telefono', 'direccion', 'condicion_fiscal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'condicion_fiscal': Select2Widget(attrs={'class': 'form-control'}),
        }
        labels = {
            'cuit': 'CUIT',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'condicion_fiscal': 'Condición Fiscal',
        }
        help_texts = {
            'cuit': 'Ingrese el CUIT sin guiones ni espacios.',
        }
        error_messages = {
            'email': {
                'invalid': 'Ingrese un correo electrónico válido.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            try:
                default_cf = CondicionFiscal.objects.get(nombre="Consumidor Final")
                self.fields['condicion_fiscal'].initial = default_cf.id
            except CondicionFiscal.DoesNotExist:
                pass

    def clean_cuit(self):
        cuit = self.cleaned_data.get('cuit')
        if not cuit.isdigit() or len(cuit) != 11:
            raise forms.ValidationError('El CUIT debe contener exactamente 11 dígitos numéricos.')
        return cuit

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.replace('+', '').replace('-', '').isdigit():
            raise forms.ValidationError('El teléfono solo puede contener números, guiones y el símbolo +.')
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if direccion:
            if not all(c.isalnum() or c.isspace() or c in ',.-#' for c in direccion):
                raise forms.ValidationError('La dirección contiene caracteres no permitidos.')
        return direccion

class VentaItemForm(forms.ModelForm):
    class Meta:
        model = VentaItem
        fields = ['producto', 'cantidad', 'precio', 'descuento']
        widgets = {
            'producto': forms.Select(attrs={'class': 'select-producto'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control precio-input', 'step': '0.01', 'min': '0'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.instance and getattr(self.instance, 'producto', None):
                self.fields['producto'].queryset = Producto.objects.filter(pk=self.instance.producto.pk)
            else:
                self.fields['producto'].queryset = Producto.objects.all()
        except Exception:
            self.fields['producto'].queryset = Producto.objects.all()


class BaseVentaItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        seen = set()
        duplicates = []
        for cd in getattr(self, 'cleaned_data', []):
            if not cd or cd.get('DELETE'):
                continue
            producto = cd.get('producto')
            if producto is None:
                continue
            if producto.id in seen:
                duplicates.append(producto)
            else:
                seen.add(producto.id)

        if duplicates:
            names = ', '.join(str(p.nombre) for p in duplicates)
            raise ValidationError(f'No puede repetir el mismo producto en la venta: {names}')


VentaItemFormSet = inlineformset_factory(Venta, VentaItem, form=VentaItemForm, formset=BaseVentaItemFormSet, extra=1, can_delete=False)

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'vendedor', 'moneda', 'comentarios', 'forma_pago', 'iva']
        widgets = {
            'cliente': Select2Widget(attrs={'class': 'form-control'}),
            'vendedor': forms.TextInput(attrs={'class': 'form-control'}),
            'moneda': Select2Widget(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'forma_pago': Select2Widget(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'iva': Select2Widget(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, 'pk', None):
            self.fields['cliente'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and getattr(self.instance, 'pk', None) and getattr(self.instance, 'completado', False):
            cleaned_data['completado'] = True

        if self.instance and getattr(self.instance, 'pk', None):
            cliente_enviado = cleaned_data.get('cliente')
            if cliente_enviado != self.instance.cliente:
                self.add_error('cliente', 'No se puede modificar el cliente de una venta ya creada.')

        return cleaned_data