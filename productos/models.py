from django.db import models

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
  marca = models.CharField(max_length=50, blank=True, null=True)
  fecha_registro = models.DateTimeField(auto_now_add=True)
  fecha_ultimo_ingreso = models.DateTimeField(null=True, blank=True)
  activo = models.BooleanField(default=True)

  class Meta:
    verbose_name = 'producto'
    verbose_name_plural = 'productos'
    ordering = ['nombre']


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