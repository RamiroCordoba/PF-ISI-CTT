from django.core.exceptions import PermissionDenied

def solo_no_vendedores(user):
    return not user.groups.filter(name='vendedor').exists()
