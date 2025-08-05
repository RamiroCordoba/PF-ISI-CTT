from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect


@login_required
def dashboard_view(request):
    return render(request, 'dashboard/principal.html')


def logout_view(request):
    logout(request)
    return redirect('login')