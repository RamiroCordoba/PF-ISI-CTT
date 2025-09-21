// JS específico para rep_ventas_generales.html

// Lógica de selección múltiple tipo checklist para vendedores y categorías
document.addEventListener('DOMContentLoaded', function() {
  // Vendedores: lógica de "Todos"
  const vendedorTodos = document.getElementById('vendedor-todos');
  if (vendedorTodos) {
    vendedorTodos.addEventListener('change', function(e) {
      document.querySelectorAll('.vendedor-check').forEach(cb => {
        cb.checked = e.target.checked;
      });
    });
    document.querySelectorAll('.vendedor-check').forEach(cb => {
      cb.addEventListener('change', function() {
        if (!this.checked) vendedorTodos.checked = false;
        else {
          const allChecked = Array.from(document.querySelectorAll('.vendedor-check')).every(c => c.checked);
          vendedorTodos.checked = allChecked;
        }
      });
    });
  }

  // Categorías: lógica de "Todas"
  const categoriaTodas = document.getElementById('categoria-todas');
  if (categoriaTodas) {
    categoriaTodas.addEventListener('change', function(e) {
      document.querySelectorAll('.categoria-check').forEach(cb => {
        cb.checked = e.target.checked;
      });
    });
    document.querySelectorAll('.categoria-check').forEach(cb => {
      cb.addEventListener('change', function() {
        if (!this.checked) categoriaTodas.checked = false;
        else {
          const allChecked = Array.from(document.querySelectorAll('.categoria-check')).every(c => c.checked);
          categoriaTodas.checked = allChecked;
        }
      });
    });
  }
});

function validarFiltrosReporte() {
  document.getElementById('error-fecha-desde').style.display = 'none';
  document.getElementById('error-fecha-hasta').style.display = 'none';
  document.getElementById('error-vendedores').style.display = 'none';
  document.getElementById('error-categorias').style.display = 'none';

  let valid = true;
  const fechaDesde = document.getElementById('fecha_desde').value;
  const fechaHasta = document.getElementById('fecha_hasta').value;
  const vendedores = Array.from(document.querySelectorAll('.vendedor-check:checked')).map(cb => cb.value);
  const todosVendedores = document.getElementById('vendedor-todos').checked;
  const categorias = Array.from(document.querySelectorAll('.categoria-check:checked')).map(cb => cb.value);
  const todasCategorias = document.getElementById('categoria-todas').checked;

  if (!fechaDesde) {
    document.getElementById('error-fecha-desde').innerText = 'La fecha desde es obligatoria';
    document.getElementById('error-fecha-desde').style.display = 'block';
    valid = false;
  }
  if (!fechaHasta) {
    document.getElementById('error-fecha-hasta').innerText = 'La fecha hasta es obligatoria';
    document.getElementById('error-fecha-hasta').style.display = 'block';
    valid = false;
  }
  if (fechaDesde && fechaHasta && fechaHasta < fechaDesde) {
    document.getElementById('error-fecha-hasta').innerText = 'La fecha hasta no puede ser menor a la fecha desde';
    document.getElementById('error-fecha-hasta').style.display = 'block';
    valid = false;
  }
  if (!todosVendedores && vendedores.length === 0) {
    document.getElementById('error-vendedores').innerText = 'Debes seleccionar al menos un vendedor';
    document.getElementById('error-vendedores').style.display = 'block';
    valid = false;
  }
  if (!todasCategorias && categorias.length === 0) {
    document.getElementById('error-categorias').innerText = 'Debes seleccionar al menos una categoría';
    document.getElementById('error-categorias').style.display = 'block';
    valid = false;
  }
  return valid;
}

// Chart.js ejemplo
window.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('ventasChart')) {
    const ctx = document.getElementById('ventasChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
        datasets: [{
          label: 'Ventas',
          data: [120, 190, 300, 250, 400],
          backgroundColor: '#F15A29',
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true },
          title: { display: true, text: 'Ventas por mes' }
        }
      }
    });
  }
});

