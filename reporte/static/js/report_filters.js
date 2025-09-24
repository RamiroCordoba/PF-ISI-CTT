// report_filters.js
// Lógica para los filtros de reportes en index_report.html

document.addEventListener('DOMContentLoaded', function() {
  // Renderizar vendedores desde API
  const vendedoresChecklist = document.getElementById('vendedores-checklist');
  fetch('/informes/reportes/vendedores_api')
    .then(response => response.json())
    .then(data => {
      data.vendedores.forEach(v => {
        const label = document.createElement('label');
        label.innerHTML = `<input type="checkbox" class="vendedor-check" value="${v.id}"> ${v.nombre}`;
        vendedoresChecklist.appendChild(label);
        vendedoresChecklist.appendChild(document.createElement('br'));
      });
    });

  // Renderizar categorías desde API
  const categoriasChecklist = document.getElementById('categorias-checklist');
  fetch('/informes/reportes/categorias_api')
    .then(response => response.json())
    .then(data => {
      data.categorias.forEach(c => {
        const label = document.createElement('label');
        label.innerHTML = `<input type="checkbox" class="categoria-check" value="${c.id}"> ${c.nombre}`;
        categoriasChecklist.appendChild(label);
        categoriasChecklist.appendChild(document.createElement('br'));
      });
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
    // Limpiar mensajes previos
    document.querySelectorAll('.filter-error').forEach(e => e.remove());

    // Recolectar valores de los filtros
    const fechaDesde = document.getElementById('fecha-desde').value;
    const fechaHasta = document.getElementById('fecha-hasta').value;
    const vendedoresSeleccionados = Array.from(document.querySelectorAll('.vendedor-check:checked')).map(cb => cb.value);
    const categoriasSeleccionadas = Array.from(document.querySelectorAll('.categoria-check:checked')).map(cb => cb.value);
    const todosVendedores = document.getElementById('vendedor-todos').checked;
    const todasCategorias = document.getElementById('categoria-todas').checked;

    let valid = true;

    // Validación fecha desde
    if (!fechaDesde) {
      showError('fecha-desde', 'La fecha desde es obligatoria');
      valid = false;
    }
    // Validación fecha hasta
    if (!fechaHasta) {
      showError('fecha-hasta', 'La fecha hasta es obligatoria');
      valid = false;
    }
    // Validación rango fechas
    if (fechaDesde && fechaHasta && fechaHasta < fechaDesde) {
      showError('fecha-hasta', 'La fecha hasta no puede ser menor a la fecha desde');
      valid = false;
    }
    // Validación vendedores
    if (!todosVendedores && vendedoresSeleccionados.length === 0) {
      showError('vendedores-checklist', 'Debes seleccionar al menos un vendedor');
      valid = false;
    }
    // Validación categorías
    if (!todasCategorias && categoriasSeleccionadas.length === 0) {
      showError('categorias-checklist', 'Debes seleccionar al menos una categoría');
      valid = false;
    }

    if (!valid) return;

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

  // Función para mostrar errores debajo de cada tarjeta
  function showError(targetId, msg) {
    const target = document.getElementById(targetId);
    if (target) {
      const error = document.createElement('div');
      error.className = 'filter-error';
      error.style.color = '#c13e0f';
      error.style.fontWeight = '500';
      error.style.fontSize = '1rem';
      error.style.marginTop = '8px';
      error.innerText = msg;
      target.parentNode.appendChild(error);
    }
  }
});
