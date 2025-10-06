from django.shortcuts import render

def custom_permission_denied_view(request, exception=None):
    return render(request, 'dashboard/403.html', status=403)
