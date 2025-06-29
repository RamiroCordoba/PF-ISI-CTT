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

  def __str__(self):
    return self.nombre