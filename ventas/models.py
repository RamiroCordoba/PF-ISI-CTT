from django.db import models
from productos.models import Producto

class Linea_Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='lineas_pedido')
    cantidad = models.PositiveIntegerField()
    observacion = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'línea de pedido'
        verbose_name_plural = 'líneas de pedido'
        ordering = ['producto']

    def __str__(self):
        return f'Producto: {self.producto.nombre} - Cantidad: {self.cantidad} - Precio Unitario: {self.producto.precio}'
    
