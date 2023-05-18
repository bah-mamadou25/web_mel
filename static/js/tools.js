/**
 * Récupère la valeur d'un cookie spécifique en fonction de son nom.
 * @param {string} name - Le nom du cookie à récupérer.
 * @return {string|null} - La valeur du cookie s'il est trouvé, ou null s'il n'existe pas.
 */


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  

  $(document).ready(function() {
    $('.toast').toast('show');
    console.log('toast')
  });


  function parseCSV(csvContent) {
    const lines = csvContent.split('\n');
    const dataArray = [];
    for (let i = 0; i < lines.length; i++) {
      dataArray.push( lines[i]);
    }
    return dataArray;
  }


  function validFromCsv(selecteur, tdIndices,parsedCSV) {
    const tbody = document.querySelector(selecteur);
    const rows = tbody.getElementsByTagName('tr');
    const dataArray = [];
  
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      const cells = row.getElementsByTagName('td');
      let rowData = '';
  
      for (let j = 0; j < tdIndices.length; j++) {
        const index = tdIndices[j];
  
        if (index >= 0 && index < cells.length) {
          if (j > 0) {
            rowData += ';';
          }
          
          rowData += cells[index].textContent.trim();
        }
      }
      
      if(parsedCSV.includes(rowData)){
        const svgElement = document.querySelectorAll(selecteur + ' ' + 'tr td:last-child svg')[i];
        const clickEvent = new Event('click');
        svgElement.dispatchEvent(clickEvent);

        dataArray.push(rowData);
      }
    }
  
    return dataArray;
  }
  
  function validFromInter(selector, min, max, numTdScoreLocated) {
    const tbody = document.querySelector(selector);
    const rows = tbody.getElementsByTagName('tr');
    const chunkSize = 100; // Nombre de lignes à traiter par lot
  
    const processChunk = (start) => {
      const end = Math.min(start + chunkSize, rows.length);
  
      for (let i = start; i < end; i++) {
        let rightTd = rows[i].querySelector('td:nth-child(' + numTdScoreLocated + ')');
        let score = parseFloat(rightTd.innerText);
  
        if (score >= min && score <= max) {
          const svgElement = document.querySelectorAll(selector + ' tr td:last-child svg')[i];
          const clickEvent = new Event('click');
          svgElement.dispatchEvent(clickEvent);
        }
      }
  
      if (end < rows.length) {
        setTimeout(() => processChunk(end), 0); // Délai de 0 millisecondes pour éviter de bloquer le navigateur
      }
    };
  
    processChunk(0); // Démarrer le traitement du premier lot
  }
  