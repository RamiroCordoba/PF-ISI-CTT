from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
  nombre = models.CharField(max_length=40, unique=True, null=False, blank=False)
  descripcion = models.TextField(null=True,blank=True)

  class Meta:
    verbose_name = 'categoria'
    verbose_name_plural = 'categorias'
    ordering = ['nombre']

  def __str__(self):
    return self.nombre

class Producto(models.Model):
  nombre = models.CharField(max_length=100, unique=True, blank=False, null=False)
  descripcion = models.TextField(blank=True, null=True)
  precio = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField(default=0)
  stock_optimo= models.PositiveIntegerField(null=False,default=0)
  stock_maximo = models.PositiveIntegerField(null=True, blank=True)
  stock_minimo = models.PositiveIntegerField(null=True, blank=True)
  categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='productos')
  marca = models.CharField(max_length=50, blank=True, null=True, default='')
  fecha_registro = models.DateTimeField(auto_now_add=True)
  fecha_ultimo_ingreso = models.DateTimeField(null=True, blank=True)
  activo = models.BooleanField(default=True)
  proveedores = models.ManyToManyField('Proveedor', related_name='productos', blank=True)
  
  class Meta:
    verbose_name = 'producto'
    verbose_name_plural = 'productos'
    ordering = ['nombre']

  def __str__(self):
    return self.nombre

class Proveedor(models.Model):
  nombreEmpresa = models.CharField(max_length=200,unique=True,blank=False,null=False)
  nombreProv  =  models.CharField(max_length=200,unique=True,blank=False,null=False)
  telefono = models.CharField(max_length=15,blank=True)
  mail = models.EmailField()
  estado = models.BooleanField(default=True)
  direccion = models.CharField(max_length=200,null=True,blank=True)
  provincia = models.CharField(max_length=50,null=True,blank=True)
  ciudad = models.CharField(max_length=50,null=True,blank=True)
  categoria = models.ManyToManyField('Categoria', related_name='proveedores')
    
  class Meta:
    verbose_name = 'Proveedor'
    verbose_name_plural = 'Proveedores'
    ordering = ['nombreEmpresa']

  
  def __str__(self):
    return self.nombreEmpresa
  

class Estacionalidad(models.Model):
  producto = models.ManyToManyField('Producto' ,related_name='estacionalidades')
  nombre = models.CharField(max_length= 200 , blank = True)
  estacion = models.CharField(max_length= 50)
  mesDesde = models.PositiveIntegerField(verbose_name='Mes Hasta',null=False, blank=False,validators=[MinValueValidator(1),MaxValueValidator(12)])
  diaHasta = models.PositiveIntegerField(verbose_name='Dia Hasta',null=False, blank=False,validators=[MinValueValidator(1),MaxValueValidator(31)])
  diaDesde = models.PositiveIntegerField(verbose_name='Dia Hasta',null=False, blank=False,validators=[MinValueValidator(1),MaxValueValidator(31)])
  mesHasta = models.PositiveIntegerField(verbose_name='Mes Hasta',null=False, blank=False,validators=[MinValueValidator(1),MaxValueValidator(12)])
  stockMin   = models.PositiveIntegerField(null=True, blank=True)
  stockMax   = models.PositiveIntegerField(null=True, blank=True)
  
  class Meta:
    verbose_name = 'Estacionalidad'
    verbose_name_plural = 'Estacionalidades'
    ordering = ['nombre']

  
  def __str__(self):
    return self.nombre


class Pedido(models.Model):
    proveedor = models.ForeignKey('Proveedor', on_delete=models.PROTECT, related_name='pedidos')
    fecha = models.DateField(auto_now_add=True)
    fechaIngreso = models.DateField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.id} a {self.proveedor.nombreEmpresa}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"