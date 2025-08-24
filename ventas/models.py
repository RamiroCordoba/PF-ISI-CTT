from django.db import models
from productos.models import Producto,FormaPago

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True, blank=False, null=False)
    apellido = models.CharField(max_length=100, unique=True, blank=False, null=False)
    razon_social = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False) 
    cuit = models.CharField(max_length=20, unique=True, blank=False, null=False)
    telefono = models.CharField(max_length=20, unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=200, unique=True, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    condicion_fiscal = models.ForeignKey('condicionfiscal', on_delete=models.PROTECT, related_name='clientes')

    class Meta:   
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class CondicionFiscal(models.Model):
    nombre = models.CharField(max_length=100, unique=True, blank=False, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    #Podria agregarse un campo descripcion e IVA asociado
    class Meta:
        verbose_name = 'condicion fiscal'
        verbose_name_plural = 'condiciones fiscales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
class Moneda(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    simbolo = models.CharField(max_length=10, unique=True, blank=False, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'moneda'
        verbose_name_plural = 'monedas'
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
    
    
class Iva(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'IVA'
        verbose_name_plural = 'IVAs'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    fecha = models.DateField(auto_now_add=True)
    vendedor = models.CharField(max_length=100, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.PROTECT, null=True, blank=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    iva = models.ForeignKey(Iva , on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} a {self.cliente.nombre}"

class Ventaitem(models.Model):
    venta = models.ForeignKey(Venta, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT) 
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
