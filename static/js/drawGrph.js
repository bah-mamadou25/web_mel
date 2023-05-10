
function drawGraphe(data){

    const intervalCount = parseInt((data.length)/100);
    const intervalSize = 1 / intervalCount;
    const intervals = Array(intervalCount).fill(0);

    data.forEach(value => {
      const intervalIndex = Math.floor(value / intervalSize);
      intervals[intervalIndex]++;
    });

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: intervals.map((_, i) => (i * intervalSize).toFixed(2)),
        datasets: [{
          label: 'Distribution des valeurs',
          data: intervals,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
}

