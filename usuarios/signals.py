from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from productos.models import Producto, Categoria

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    vendedor, _ = Group.objects.get_or_create(name='vendedor')
    administrador, _ = Group.objects.get_or_create(name='administrador')

    permisos_vendedor = Permission.objects.filter(
        content_type__in=ContentType.objects.get_for_models(Producto, Categoria).values(),
        codename__startswith='view_'
    )
    vendedor.permissions.set(permisos_vendedor)
