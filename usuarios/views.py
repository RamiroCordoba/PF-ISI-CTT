from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RegistroForm

class UsuarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    permission_required = 'auth.view_user'

class UsuarioCreateView(CreateView):
    model = User
    form_class = RegistroForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        grupo = form.cleaned_data['grupo']
        user.groups.add(grupo)  # Asigna el grupo al usuario
        return super().form_valid(form)
