/**
 * Convertit le contenu d'un élément <tbody> en format CSV.
 * @param {HTMLElement} tbodyElement - L'élément <tbody> contenant les lignes et les colonnes à convertir en CSV.
 * @returns {string} - Le contenu converti au format CSV.
 */
function convertTbodyToCSV(tbodyElement) {
    // Récupérer toutes les lignes du tbody
    const rows = tbodyElement.querySelectorAll('tr');
    
    // Créer un tableau pour stocker les données CSV
    const csvData = [];
    
    // Parcourir chaque ligne
    rows.forEach((row) => {
      const rowData = [];
      
      // Récupérer toutes les colonnes (td) de la ligne
      const columns = row.querySelectorAll('td');
      
      // Parcourir chaque colonne
      for (let i = 1; i < 4; i++) {
        const columnData = columns[i].textContent.trim();
        rowData.push(columnData);
      }
      
      // Ajouter la ligne au tableau de données CSV
      csvData.push(rowData);
    });
    
    // Convertir le tableau de données CSV en format CSV
    const csvString = csvData.map(row => row.join(';')).join('\n');
    
    return csvString;
  }
  
  /**
   * Télécharge le contenu CSV en tant que fichier.
   * @param {string} csvContent - Le contenu CSV à télécharger.
   * @param {string} fileName - Le nom du fichier CSV résultant.
   */
  function downloadCSVFile(csvContent, fileName) {
    const encodedCSVContent = encodeURIComponent(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodedCSVContent);
    link.setAttribute('download', fileName);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  
  /**
   * Écouteur d'événement pour le bouton de téléchargement associé à l'élément avec l'id 'attente'.
   * Convertit le contenu du tbody correspondant en CSV et télécharge le fichier.
   */
  $(".download-att").click(function() {
    downloadCSVFile(convertTbodyToCSV(document.querySelector('#attente tbody')),
                    'termes_attentes.csv');
  });
  
  /**
   * Écouteur d'événement pour le bouton de téléchargement associé à l'élément avec l'id 'valider'.
   * Convertit le contenu du tbody correspondant en CSV et télécharge le fichier.
   */
  $(".download-val").click(function() {
    downloadCSVFile(convertTbodyToCSV(document.querySelector('#valider tbody')),
                    'termes_validés.csv');
  });
  
  /**
   * Écouteur d'événement pour le bouton de téléchargement associé à l'élément avec l'id 'supprimer'.
   * Convertit le contenu du tbody correspondant en CSV et télécharge le fichier.
   */
  $(".download-sup").click(function() {
    downloadCSVFile(convertTbodyToCSV(document.querySelector('#supprimer tbody')),
                    'termes_supprimés.csv');
  });
  