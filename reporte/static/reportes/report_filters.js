// report_filters.js
// Lógica para los filtros de reportes en index_report.html

document.addEventListener('DOMContentLoaded', function() {
  // Simulación: vendedores y categorías (reemplazar por datos reales si se usan AJAX/Django)
  const vendedores = [
    { id: 1, nombre: 'Juan Pérez' },
    { id: 2, nombre: 'Ana Gómez' },
    { id: 3, nombre: 'Carlos Ruiz' }
  ];
  const categorias = [
    { id: 1, nombre: 'Herramientas' },
    { id: 2, nombre: 'Materiales' },
    { id: 3, nombre: 'Pinturas' }
  ];

  // Renderizar vendedores
  const vendedoresChecklist = document.getElementById('vendedores-checklist');
  vendedores.forEach(v => {
    const label = document.createElement('label');
    label.innerHTML = `<input type="checkbox" class="vendedor-check" value="${v.id}"> ${v.nombre}`;
    vendedoresChecklist.appendChild(label);
    vendedoresChecklist.appendChild(document.createElement('br'));
  });

  // Renderizar categorías
  const categoriasChecklist = document.getElementById('categorias-checklist');
  categorias.forEach(c => {
    const label = document.createElement('label');
    label.innerHTML = `<input type="checkbox" class="categoria-check" value="${c.id}"> ${c.nombre}`;
    categoriasChecklist.appendChild(label);
    categoriasChecklist.appendChild(document.createElement('br'));
  });

  // Lógica de "Todos" vendedores
  document.getElementById('vendedor-todos').addEventListener('change', function(e) {
    document.querySelectorAll('.vendedor-check').forEach(cb => {
      cb.checked = e.target.checked;
    });
  });
  // Lógica de "Todas" categorías
  document.getElementById('categoria-todas').addEventListener('change', function(e) {
    document.querySelectorAll('.categoria-check').forEach(cb => {
      cb.checked = e.target.checked;
    });
  });

  // Botón generar reporte
  document.getElementById('btn-generar-reporte').addEventListener('click', function() {
    // Recolectar valores de los filtros
    const fechaDesde = document.getElementById('fecha-desde').value;
    const fechaHasta = document.getElementById('fecha-hasta').value;
    const vendedoresSeleccionados = Array.from(document.querySelectorAll('.vendedor-check:checked')).map(cb => cb.value);
    const categoriasSeleccionadas = Array.from(document.querySelectorAll('.categoria-check:checked')).map(cb => cb.value);
    // Si "Todos" está seleccionado, enviar todos los vendedores
    const todosVendedores = document.getElementById('vendedor-todos').checked;
    // Si "Todas" está seleccionado, enviar todas las categorías
    const todasCategorias = document.getElementById('categoria-todas').checked;

    // Construir parámetros GET
    const params = new URLSearchParams();
    if (fechaDesde) params.append('fecha_desde', fechaDesde);
    if (fechaHasta) params.append('fecha_hasta', fechaHasta);
    if (todosVendedores) {
      params.append('vendedores', 'todos');
    } else {
      vendedoresSeleccionados.forEach(v => params.append('vendedores', v));
    }
    if (todasCategorias) {
      params.append('categorias', 'todas');
    } else {
      categoriasSeleccionadas.forEach(c => params.append('categorias', c));
    }
    // Redirigir con parámetros
  window.location.href = '/informes/reportes/rep_ventas_generales?' + params.toString();
  });
});
