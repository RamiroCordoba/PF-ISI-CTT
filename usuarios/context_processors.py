def rol_usuario(request):
    user = getattr(request, 'user', None)
    es_vendedor = False
    if user and user.is_authenticated:
        # Solo es vendedor si está en el grupo vendedor y NO es staff ni superuser
        # Si el usuario es admin o superadmin (aunque esté en vendedor), NO se lo limita
        es_vendedor = user.groups.filter(name='vendedor').exists() and not (user.is_staff or user.is_superuser)
    return {'es_vendedor': es_vendedor}  # True solo si es vendedor puro
