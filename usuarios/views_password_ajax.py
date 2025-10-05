from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views import View

class PasswordChangeAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return JsonResponse({'success': True})
            else:
                # Devolver errores de los campos
                errors = {field: error for field, error in form.errors.items()}
                return JsonResponse({'success': False, 'error': errors})
        return JsonResponse({'success': False, 'error': 'Petición inválida'}, status=400)
