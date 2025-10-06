from django.core.exceptions import PermissionDenied

def solo_no_vendedores(user):
    # Solo restringe si es vendedor y no es staff ni superuser
    return not (user.groups.filter(name='vendedor').exists() and not (user.is_staff or user.is_superuser))
