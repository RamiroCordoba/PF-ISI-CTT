from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from productos.models import Producto, Categoria
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    if sender.name != "usuarios":
        return

    vendedor, _ = Group.objects.get_or_create(name='vendedor')
    administrador, _ = Group.objects.get_or_create(name='administrador')

    permisos_vendedor = Permission.objects.filter(
        content_type__in=ContentType.objects.get_for_models(Producto, Categoria).values(),
        codename__startswith='view_'
    )
    vendedor.permissions.set(permisos_vendedor)

    # Ajustar is_staff según grupo asignado
    User = get_user_model()
    # Vendedores: is_staff = False
    for user in User.objects.filter(groups__name='vendedor'):
        if user.is_staff:
            user.is_staff = False
            user.save(update_fields=['is_staff'])
    # Administradores: is_staff = True
    for user in User.objects.filter(groups__name='administrador'):
        if not user.is_staff:
            user.is_staff = True
            user.save(update_fields=['is_staff'])