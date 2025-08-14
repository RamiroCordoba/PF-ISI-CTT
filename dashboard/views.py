from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Sum
from productos.models import PedidoItem

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/principal.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def top_10_productos_mas_pedidos(request):
    datos = (
        PedidoItem.objects
        .values('producto__nombre')
        .annotate(total=Sum('cantidad'))
        .order_by('-total')[:10]
    )
    labels = [item['producto__nombre'] or 'Sin nombre' for item in datos]
    data = [item['total'] for item in datos]
    return JsonResponse({'labels': labels, 'data': data})
