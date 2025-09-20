from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'reportes/index_report.html')

def rep_ventas_generales_view(request):
    # Obtener parámetros GET
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    vendedores = request.GET.getlist('vendedores')
    categorias = request.GET.getlist('categorias')
    context = {
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'vendedores': vendedores,
        'categorias': categorias,
    }
    return render(request, 'reportes/rep_ventas_generales.html', context)