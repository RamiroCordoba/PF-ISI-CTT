from django.db import models
from productos.models import Producto,FormaPago
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.db.models import F
from django.db import transaction
from django.db.models import ProtectedError
import logging

logger = logging.getLogger(__name__)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100,  blank=False, null=False)
    apellido = models.CharField(max_length=100, blank=False, null=False)
    razon_social = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=False, null=False) 
    cuit = models.CharField(max_length=11, unique=True, blank=False, null=False)
    telefono = models.CharField(max_length=20,  blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
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
    iva = models.ForeignKey(Iva , on_delete=models.PROTECT, null=True, blank=True)
    completado = models.BooleanField(default=False)
    stock_actualizado = models.BooleanField(default=False)
    anulada = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.id} a {self.cliente.nombre}"

    def delete(self, *args, **kwargs):
        if self.anulada:
            return

        try:
            from .models import create_nota_from_venta, apply_stock_for_nota  
        except Exception:
            self.anulada = True
            self.save(update_fields=['anulada'])
            return

        try:
            with transaction.atomic():
                if self.completado:
                    nota = create_nota_from_venta(self)
                    if nota is not None:
                        apply_stock_for_nota(nota)

                self.anulada = True
                self.save(update_fields=['anulada'])
        except Exception:
            logger.exception("Error creating/applying NotaCredito during Venta.delete for venta %s", getattr(self, 'pk', None))
            try:
                self.anulada = True
                self.save(update_fields=['anulada'])
            except Exception:
                pass
        return

class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT) 
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    stock_aplicado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['venta', 'producto'], name='unique_venta_producto')
        ]



@receiver(pre_save, sender=Venta)
def venta_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            prev = Venta.objects.get(pk=instance.pk)
            instance._prev_completado = prev.completado
        except Venta.DoesNotExist:
            instance._prev_completado = False
    else:
        instance._prev_completado = False


@receiver(post_save, sender=Venta)
def venta_post_save(sender, instance, created, **kwargs):
    prev = getattr(instance, '_prev_completado', False)
    if not created and (not prev) and instance.completado:
        def _apply():
            unapplied = instance.items.filter(stock_aplicado=False).select_related('producto')
            for item in unapplied:
                Producto.objects.filter(pk=item.producto_id).update(
                    stock=F('stock') - (item.cantidad or 0),
                    fecha_ultimo_ingreso=timezone.now()
                )
                VentaItem.objects.filter(pk=item.pk).update(stock_aplicado=True)
            remaining = instance.items.filter(stock_aplicado=False).exists()
            if not remaining:
                Venta.objects.filter(pk=instance.pk).update(stock_actualizado=True)

        try:
            transaction.on_commit(_apply)
        except Exception:
            _apply()


@receiver(post_save, sender=VentaItem)
def ventaitem_post_save(sender, instance, created, **kwargs):
    venta = instance.venta
    needs_apply = VentaItem.objects.filter(pk=instance.pk, stock_aplicado=False).exists()
    if venta.completado and needs_apply:
        def _apply_item():
            Producto.objects.filter(pk=instance.producto_id).update(
                stock=F('stock') - (instance.cantidad or 0),
                fecha_ultimo_ingreso=timezone.now()
            )
            VentaItem.objects.filter(pk=instance.pk).update(stock_aplicado=True)
            remaining = venta.items.filter(stock_aplicado=False).exists()
            if not remaining:
                Venta.objects.filter(pk=venta.pk).update(stock_actualizado=True)

        try:
            transaction.on_commit(_apply_item)
        except Exception:
            _apply_item()


def apply_stock_for_venta(venta):

    from django.db import transaction
    unapplied = list(venta.items.filter(stock_aplicado=False).select_related('producto'))
    if not unapplied:
        return

    from django.db import transaction
    with transaction.atomic():

        product_ids = [item.producto_id for item in unapplied]
        productos = {p.id: p for p in Producto.objects.select_for_update().filter(pk__in=product_ids)}


        insufficient = []
        for item in unapplied:
            prod = productos.get(item.producto_id)
            if prod is None:
                insufficient.append((item.producto_id, 'no existe'))
            else:
                if (prod.stock or 0) < (item.cantidad or 0):
                    insufficient.append((prod.nombre, prod.stock, item.cantidad))

        if insufficient:
            logger.info("apply_stock_for_venta aborted for venta %s: insufficient=%s", getattr(venta, 'pk', None), insufficient)
            return

        for item in unapplied:
            Producto.objects.filter(pk=item.producto_id).update(
                stock=F('stock') - (item.cantidad or 0),
                fecha_ultimo_ingreso=timezone.now()
            )
            VentaItem.objects.filter(pk=item.pk).update(stock_aplicado=True)

        remaining = venta.items.filter(stock_aplicado=False).exists()
        if not remaining:
            Venta.objects.filter(pk=venta.pk).update(stock_actualizado=True)

        logger.info("apply_stock_for_venta applied %d items for venta %s", len(unapplied), getattr(venta, 'pk', None))


def revert_stock_for_venta(venta):

    from django.db import transaction
    applied_items = list(venta.items.filter(stock_aplicado=True).select_related('producto'))
    if not applied_items:
        return 0

    with transaction.atomic():
        product_ids = [it.producto_id for it in applied_items]
        productos = {p.id: p for p in Producto.objects.select_for_update().filter(pk__in=product_ids)}

        for item in applied_items:
            prod = productos.get(item.producto_id)
            if prod is None:
                continue
            try:
                logger.warning("Reverting stock for venta %s: producto_id=%s cantidad=%s stock_before=%s", getattr(venta,'pk',None), item.producto_id, item.cantidad, getattr(prod,'stock',None))
            except Exception:
                pass
            Producto.objects.filter(pk=item.producto_id).update(
                stock=F('stock') + (item.cantidad or 0),
                fecha_ultimo_ingreso=timezone.now()
            )

            VentaItem.objects.filter(pk=item.pk).update(stock_aplicado=False)


        Venta.objects.filter(pk=venta.pk).update(stock_actualizado=False)

    logger.info("revert_stock_for_venta reverted %d items for venta %s", len(applied_items), getattr(venta, 'pk', None))
    return len(applied_items)
    

class NotaCredito(models.Model):

    venta_original = models.ForeignKey(Venta, null=True, blank=True, on_delete=models.SET_NULL, related_name='notas_credito')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='notas_credito')
    fecha = models.DateField(auto_now_add=True)
    comentarios = models.TextField(null=True, blank=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, null=True, blank=True)
    iva = models.ForeignKey(Iva , on_delete=models.PROTECT, null=True, blank=True)
    aplicado = models.BooleanField(default=False)

    def __str__(self):
        return f"NotaCredito #{self.id} ref Venta #{getattr(self.venta_original, 'id', 'N/A')}"

    @property
    def total(self):
        total = Decimal('0')
        for it in self.items.all():
            try:
                precio = Decimal(str(it.precio)) if it.precio is not None else Decimal('0')
            except Exception:
                precio = Decimal('0')
            try:
                cantidad = Decimal(str(it.cantidad)) if it.cantidad is not None else Decimal('0')
            except Exception:
                cantidad = Decimal('0')
            try:
                descuento_pct = Decimal(str(it.descuento or 0))
            except Exception:
                descuento_pct = Decimal('0')
            descuento_factor = Decimal('1') - (descuento_pct / Decimal('100'))
            subtotal = (precio * cantidad * descuento_factor)
            total += subtotal
        return total


class NotaCreditoItem(models.Model):
    nota = models.ForeignKey(NotaCredito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    stock_aplicado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} (nota {getattr(self.nota, 'id', None)})"

    @property
    def subtotal(self):
        try:
            precio = Decimal(str(self.precio)) if self.precio is not None else Decimal('0')
        except Exception:
            precio = Decimal('0')
        try:
            cantidad = Decimal(str(self.cantidad)) if self.cantidad is not None else Decimal('0')
        except Exception:
            cantidad = Decimal('0')
        try:
            descuento_pct = Decimal(str(self.descuento or 0))
        except Exception:
            descuento_pct = Decimal('0')
        descuento_factor = Decimal('1') - (descuento_pct / Decimal('100'))
        return (precio * cantidad * descuento_factor)


def create_nota_from_venta(venta, comentarios=None):

    existing = NotaCredito.objects.filter(venta_original=venta).first()
    if existing:
        return existing

    with transaction.atomic():
        nota = NotaCredito.objects.create(
            venta_original=venta,
            cliente=venta.cliente,
            comentarios=comentarios or f"Nota de crédito generada por eliminación de Venta #{venta.id}",
            moneda=venta.moneda,
            iva=venta.iva,
            aplicado=False
        )
        items = []
        for it in venta.items.all():
            NotaCreditoItem.objects.create(
                nota=nota,
                producto=it.producto,
                cantidad=it.cantidad,
                precio=it.precio,
                descuento=it.descuento
            )
    logger.info("create_nota_from_venta created nota %s for venta %s", nota.pk, getattr(venta, 'pk', None))
    return nota


def apply_stock_for_nota(nota):

    applied = list(nota.items.filter(stock_aplicado=False).select_related('producto'))
    if not applied:
        return 0

    with transaction.atomic():
        product_ids = [it.producto_id for it in applied]
        productos = {p.id: p for p in Producto.objects.select_for_update().filter(pk__in=product_ids)}

        for item in applied:
            prod = productos.get(item.producto_id)
            if prod is None:
                continue
            Producto.objects.filter(pk=item.producto_id).update(
                stock=F('stock') + (item.cantidad or 0),
                fecha_ultimo_ingreso=timezone.now()
            )
            NotaCreditoItem.objects.filter(pk=item.pk).update(stock_aplicado=True)

        NotaCredito.objects.filter(pk=nota.pk).update(aplicado=True)

    logger.info("apply_stock_for_nota applied %d items for nota %s", len(applied), getattr(nota, 'pk', None))
    return len(applied)
