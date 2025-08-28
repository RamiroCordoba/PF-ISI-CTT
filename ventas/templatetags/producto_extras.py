# templatetags/producto_extras.py
from django import template
from ventas.models import Producto

register = template.Library()

@register.filter
def get_producto_nombre(producto_id):
    try:
        return Producto.objects.get(pk=int(producto_id)).nombre
    except (Producto.DoesNotExist, ValueError, TypeError):
        return ''
