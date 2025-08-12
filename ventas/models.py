from django.db import models
from productos.models import Producto

class LineaPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='lineas_pedido')
    cantidad = models.PositiveIntegerField()
    observacion = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'línea de pedido'
        verbose_name_plural = 'líneas de pedido'
        ordering = ['producto']

    def __str__(self):
        return f'Producto: {self.producto.nombre} - Cantidad: {self.cantidad} - Precio Unitario: {self.producto.precio}'
    

    
class Venta(models.Model):
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    completa = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    formaPago = models.CharField(max_length=50, choices=[
        ('EFECTIVO', 'Efectivo'),
        ('CREDITO', 'Crédito'),
        ('DEBITO', 'Débito'),
        ('TRANSFERENCIA', 'Transferencia'),
    ])
    nombreCliente = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        ordering = ['-fecha']  # Ordeno por fecha descendente

    def __str__(self):
        return f'Venta ID: {self.id} - Cliente: {self.nombreCliente or "Consumidor Final"} - Fecha: {self.fecha.strftime("%d/%m/%Y")}'
    
