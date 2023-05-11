
function drawGraphe(data) {
  const min = Math.min(...data);
  const max = Math.max(...data);
  const intervalCount = 10;
  const intervalSize = (max - min) / intervalCount;
  const intervals = Array(intervalCount).fill(0);
  const intervalLabels = [];

  data.forEach(value => {
    if (value >= min && value <= max) {
      const intervalIndex = Math.floor((value - min) / intervalSize);
      intervals[intervalIndex]++;
    }
  });

  for (let i = 0; i < intervalCount; i++) {
    const lowerBound = min + i * intervalSize;
    const upperBound = min + (i + 1) * intervalSize;
    intervalLabels.push(`${lowerBound.toFixed(3)} - ${upperBound.toFixed(3)}`);
  }

  const ctx = document.getElementById('myChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: intervalLabels,
      datasets: [{
        label: 'Nombre de valeurs',
        data: intervals,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        x: {
          title: {
            display: true,
            text: 'Intervalles'
          }
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Nombre de valeurs'
          }
        }
      }
    }
  });
}

