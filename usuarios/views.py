from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RegistroForm, UsuarioEditForm
from .models import UsuarioPersonalizado
from django.db.models import Q
from django.contrib.auth.models import Group

#________ Usuarios del sistema
def get_or_create_superadmin_group():
    group, created = Group.objects.get_or_create(name='Superadmin')
    return group

class UsuarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UsuarioPersonalizado
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    permission_required = 'auth.view_user'
    paginate_by = 10

    def get_queryset(self):
        queryset = UsuarioPersonalizado.objects.all().order_by('id')
        request = self.request

        # Asegura que el grupo Superadmin exista
        superadmin_group = get_or_create_superadmin_group()

        # Filtro por estado
        filtro_estados = request.GET.getlist('estado')
        if filtro_estados:
            estados = []
            if 'activos' in filtro_estados:
                estados.append(True)
            if 'inactivos' in filtro_estados:
                estados.append(False)
            queryset = queryset.filter(is_active__in=estados)

        # Filtro por grupo/rol
        filtro_roles = request.GET.getlist('rol')
        if filtro_roles:
            queryset = queryset.filter(groups__id__in=filtro_roles)

        # Buscador por texto
        buscar = request.GET.get('buscar', '').strip()
        if buscar:
            queryset = queryset.filter(
                Q(username__icontains=buscar) |
                Q(first_name__icontains=buscar) |
                Q(last_name__icontains=buscar) |
                Q(email__icontains=buscar)
            )

        # Añadir visualmente el grupo Superadmin a los superusuarios
        for user in queryset:
            if user.is_superuser and superadmin_group not in user.groups.all():
                user.groups.add(superadmin_group)

        queryset = queryset.distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        # Asegura que el grupo Superadmin esté en la lista de roles
        roles = list(Group.objects.all())
        superadmin_group = get_or_create_superadmin_group()
        if superadmin_group not in roles:
            roles.append(superadmin_group)
        context['filtro_estados'] = request.GET.getlist('estado')
        context['filtro_roles'] = request.GET.getlist('rol')
        context['buscar'] = request.GET.get('buscar', '')
        context['roles'] = roles
        context['filtros_activos'] = bool(context['filtro_estados'] or context['filtro_roles'])
        return context

class UsuarioCreateView(CreateView):
    model = UsuarioPersonalizado
    form_class = RegistroForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        grupos = form.cleaned_data['grupos']
        user.groups.set(grupos)
        return super().form_valid(form)
    

class UsuarioUpdateView(UpdateView):
    model = UsuarioPersonalizado
    form_class = UsuarioEditForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')

    def get_initial(self):
        initial = super().get_initial()
        initial['grupos'] = self.object.groups.all()
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.set(form.cleaned_data['grupos'])
        return response

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        from django.urls import reverse
        if next_url == 'mi_perfil':
            return reverse('usuarios:mi_perfil')
        return super().get_success_url()

class UsuarioDeleteView(DeleteView):
    model = UsuarioPersonalizado
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')

class UsuarioDetailView(DetailView):
    model = UsuarioPersonalizado
    template_name = 'usuarios/usuario_details.html'
    context_object_name = 'usuario'

class UsuarioPerfilView(DetailView):
    model = UsuarioPersonalizado
    template_name = 'usuarios/usuario_miperfil.html'
    context_object_name = 'usuario'

    def get_object(self, queryset=None):
        return self.request.user