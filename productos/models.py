from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.db.models import F
from django.db import transaction

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
  vendedor = models.CharField(max_length=100, blank=True, null=True)
  moneda = models.ForeignKey('ventas.Moneda', on_delete=models.PROTECT, null=True, blank=True)
  fecha = models.DateField(auto_now_add=True)
  fechaIngreso = models.DateField(null=True, blank=True)
  comentarios = models.TextField(null=True, blank=True)
  completado = models.BooleanField(default=False)
  stock_actualizado = models.BooleanField(default=False)
  eliminado = models.BooleanField(default=False)
  forma_pago = models.ForeignKey('FormaPago', on_delete=models.PROTECT, null=True, blank=True)
  fechaEstimadaEntrega = models.DateField(null=True, blank=True)
  def __str__(self):
    return f"Pedido #{self.id} a {self.proveedor.nombreEmpresa}"


  def delete(self, using=None, keep_parents=False):

    self.eliminado = True
    self.save(update_fields=['eliminado'])

  def hard_delete(self, using=None, keep_parents=False):
    return super(Pedido, self).delete(using=using, keep_parents=keep_parents)


class PedidoQuerySet(models.QuerySet):
  def delete(self):
    return self.update(eliminado=True)


class PedidoManager(models.Manager):
  def get_queryset(self):
    return PedidoQuerySet(self.model, using=self._db)


Pedido.add_to_class('objects', PedidoManager())
Pedido.add_to_class('all_objects', models.Manager())


class PedidoItem(models.Model):
  pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
  producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
  cantidad = models.PositiveIntegerField()
  precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  stock_aplicado = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.producto.nombre} x {self.cantidad}"



@receiver(pre_save, sender=Pedido)
def pedido_pre_save(sender, instance, **kwargs):
  if instance.pk:
    try:
      prev = Pedido.objects.get(pk=instance.pk)
      instance._prev_completado = prev.completado
    except Pedido.DoesNotExist:
      instance._prev_completado = False
  else:
    instance._prev_completado = False


@receiver(post_save, sender=Pedido)
def pedido_post_save(sender, instance, created, **kwargs):
  prev = getattr(instance, '_prev_completado', False)
  if not created and (not prev) and instance.completado:
    def _apply():
      unapplied_items = instance.items.select_related('producto').filter(stock_aplicado=False)
      for item in unapplied_items:
        Producto.objects.filter(pk=item.producto_id).update(
          stock=F('stock') + (item.cantidad or 0),
          fecha_ultimo_ingreso=timezone.now()
        )
        PedidoItem.objects.filter(pk=item.pk).update(stock_aplicado=True)
      remaining = instance.items.filter(stock_aplicado=False).exists()
      if not remaining:
        Pedido.objects.filter(pk=instance.pk).update(stock_actualizado=True)

    try:
      transaction.on_commit(_apply)
    except Exception:
      _apply()


@receiver(post_save, sender=PedidoItem)
def pedidoitem_post_save(sender, instance, created, **kwargs):
  pedido = instance.pedido
  needs_apply = PedidoItem.objects.filter(pk=instance.pk, stock_aplicado=False).exists()
  if pedido.completado and needs_apply:
    def _apply_item():
      Producto.objects.filter(pk=instance.producto_id).update(
        stock=F('stock') + (instance.cantidad or 0),
        fecha_ultimo_ingreso=timezone.now()
      )
      PedidoItem.objects.filter(pk=instance.pk).update(stock_aplicado=True)
      remaining = pedido.items.filter(stock_aplicado=False).exists()
      if not remaining:
        Pedido.objects.filter(pk=pedido.pk).update(stock_actualizado=True)

    try:
      transaction.on_commit(_apply_item)
    except Exception:
      _apply_item()


def apply_stock_for_pedido(pedido):
  from django.db import transaction
  unapplied = pedido.items.filter(stock_aplicado=False).select_related('producto')
  with transaction.atomic():
    for item in unapplied:
      Producto.objects.filter(pk=item.producto_id).update(
        stock=F('stock') + (item.cantidad or 0),
        fecha_ultimo_ingreso=timezone.now()
      )
      PedidoItem.objects.filter(pk=item.pk).update(stock_aplicado=True)
    remaining = pedido.items.filter(stock_aplicado=False).exists()
    if not remaining:
      Pedido.objects.filter(pk=pedido.pk).update(stock_actualizado=True)


def revert_stock_for_pedido(pedido):
  from django.db import transaction
  applied_items = pedido.items.filter(stock_aplicado=True).select_related('producto')
  reverted_count = applied_items.count()
  with transaction.atomic():
    for item in applied_items:
      Producto.objects.filter(pk=item.producto_id).update(
        stock=F('stock') - (item.cantidad or 0),
        fecha_ultimo_ingreso=timezone.now()
      )
      PedidoItem.objects.filter(pk=item.pk).update(stock_aplicado=False)
    Pedido.objects.filter(pk=pedido.pk).update(stock_actualizado=False)
  return reverted_count


@receiver(pre_delete, sender=Pedido)
def pedido_pre_delete(sender, instance, **kwargs):
  try:
    applied_exists = instance.items.filter(stock_aplicado=True).exists()
    if applied_exists:
      revert_stock_for_pedido(instance)
  except Exception:
    pass
    

class FormaPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Forma de Pago'
        verbose_name_plural = 'Formas de Pago'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre  