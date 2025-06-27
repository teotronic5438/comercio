function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('collapsed');
}



// Logica para los graficos estadisticos
// Paso 1: Obtener los datos JSON que Django nos envió
const datosGraficoTipo = JSON.parse('{{ datos_grafico_tipo_json|escapejs }}');
const datosGraficoDestino = JSON.parse('{{ datos_grafico_destino_json|escapejs }}');

// Función para crear un gráfico de dona. Ahora siempre compara contra un total.
function createDoughnutChart(canvasId, mainLabel, dataValue, backgroundColor, borderColor, totalCompareValue) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // El "resto" ahora siempre será el total de comparación menos el valor principal
    const remainingValue = totalCompareValue - dataValue;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            // Las etiquetas serán el nombre del segmento principal y 'Resto'
            labels: [mainLabel, 'Resto'],
            datasets: [{
                label: 'Cantidad',
                data: [dataValue, remainingValue], // Aquí se calcula el resto
                backgroundColor: [backgroundColor, 'rgba(200, 200, 200, 0.4)'], // Color para el valor y un gris para el resto
                borderColor: [borderColor, 'rgba(200, 200, 200, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: { display: false }, // El título ya está en el H2
                legend: {
                    display: true,
                    position: 'bottom' // Posición de la leyenda
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            let label = tooltipItem.label || '';
                            if (label === 'Resto') { // Si es el segmento "Resto"
                                return `Resto: ${tooltipItem.raw}`;
                            }
                            // Si es el segmento principal
                            const value = tooltipItem.raw;
                            const total = totalCompareValue; // Usamos el total de comparación
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(2) : 0;
                            return `${mainLabel}: ${value} (${percentage}%)`; // Texto como "Equipos Nuevos: 2 (20.00%)"
                        }
                    }
                }
            }
        }
    });
}

// --- GRÁFICOS DEL PRIMER GRUPO (Tipo/Estado General) ---
// Todos estos se comparan contra 'datosGraficoTipo.total_activas'
const totalOrdenesActivas = datosGraficoTipo.total_activas; // Guardamos en una variable para mayor claridad

// Gráfico 1: Total de Órdenes Activas
createDoughnutChart(
    'totalOrdenesActivasChart',
    'Total Activas', // Etiqueta principal
    totalOrdenesActivas, // Valor del segmento principal
    'rgba(75, 192, 192, 0.7)',
    'rgba(75, 192, 192, 1)',
    totalOrdenesActivas // El total de comparación es el mismo valor para este gráfico
);

// Gráfico 2: Órdenes Pendientes de Revisión Activas
createDoughnutChart(
    'pendientesRevisionActivasChart',
    'Pendientes',
    datosGraficoTipo.pendientes_revision_activas,
    'rgba(255, 99, 132, 0.7)',
    'rgba(255, 99, 132, 1)',
    totalOrdenesActivas // El total de comparación es el total de órdenes activas
);

// Gráfico 3: Órdenes Revisadas/Palletizadas Activas
createDoughnutChart(
    'revisadasPalletizadasActivasChart',
    'Revisadas/Palletizadas',
    datosGraficoTipo.revisadas_activas,
    'rgba(54, 162, 235, 0.7)',
    'rgba(54, 162, 235, 1)',
    totalOrdenesActivas // El total de comparación es el total de órdenes activas
);

// --- GRÁFICOS DEL SEGUNDO GRUPO (Por Destino) ---
// Ahora, estos también se comparan contra 'totalOrdenesActivas'
// Asegúrate de que 'totalOrdenesActivas' está definida antes de usarse aquí.

createDoughnutChart(
    'destinoNuevoActivasChart',
    'Equipos Nuevos', // Etiqueta más descriptiva
    datosGraficoDestino.destino_nuevo_activas,
    'rgba(255, 206, 86, 0.7)',
    'rgba(255, 206, 86, 1)',
    totalOrdenesActivas // ¡Aquí está el cambio clave! Se compara con el total de órdenes activas.
);

createDoughnutChart(
    'destinoAveriaActivasChart',
    'Equipos Avería',
    datosGraficoDestino.destino_averia_activas,
    'rgba(153, 102, 255, 0.7)',
    'rgba(153, 102, 255, 1)',
    totalOrdenesActivas // ¡Aquí está el cambio clave!
);

createDoughnutChart(
    'destinoDestruccionActivasChart',
    'Equipos Destrucción',
    datosGraficoDestino.destino_destruccion_activas,
    'rgba(255, 159, 64, 0.7)',
    'rgba(255, 159, 64, 1)',
    totalOrdenesActivas // ¡Aquí está el cambio clave!
);