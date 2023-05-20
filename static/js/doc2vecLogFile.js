//log à true si c'est pour les stats prend pas en compte si l'élément est validé ou pas

function convertTbodyToCSV(tbodyElement, log) {
    const rows = tbodyElement.querySelectorAll('tr');
    const csvData = [];
  
    rows.forEach((row) => {
      const rowData = [];
      const tdWithCheckedInput = row.querySelector('td > input[type="checkbox"]:checked');
      const columns = row.querySelectorAll('td');
  
      for (let column of columns) {
        const content = column.innerText.trim();
        if (content !== '' && content !== 'voir') {
          if(!log && tdWithCheckedInput){
            rowData.push(content);
          }else if(log){
            rowData.push(content);

          }
          
        }
      }
  
      if (log) {
        if (tdWithCheckedInput) {
          rowData.push('checked');
        } else {
          rowData.push('notchecked');
        }
      }
  
      if (rowData.length > 0) {
        csvData.push(rowData);
      }
    });
  
    const csvString = csvData.map((row) => row.join(';')).join('\n');
    
    return csvString;
  }

    /**
   * Télécharge le contenu CSV en tant que fichier ou  soummet le ficier en entier vers logFile.
   * @param {string} csvContent - Le contenu CSV à télécharger.
   * @param {string} fileName - Le nom du fichier CSV résultant.
   */
    function downloadCSVFile(csvContent, fileName,log) {

        if(log){
            fetchForLogModif(csvContent);

        }else{

            const encodedCSVContent = encodeURIComponent(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodedCSVContent);
            link.setAttribute('download', fileName);
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link)

        }


        
       

      }





/**
 * Envoie le contenu d'un fichier via une requête POST à une URL spécifiée.
 * @param {string} fileContent - Le contenu du fichier à envoyer.
 * @param {string} url - L'URL de destination pour l'envoi du contenu.
 */
async function fetchForLogModif(fileContent) {

    const baseUrl = window.location.origin;
    const apiEndpoint = "logFile/";
    
    const apiUrl = new URL(apiEndpoint, baseUrl).href;
    
    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: JSON.stringify({ contenu: fileContent }),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')

        }
      });
  
      if (response.ok) {
        console.log('Contenu du fichier envoyé avec succès.');
        
      } else {
        throw new Error('Erreur lors de l\'envoi du contenu du fichier.');
      }
    } catch (error) {
      console.error('Erreur lors de l\'envoi du contenu du fichier:', error);
      
    }
  }























$('#telecharger').click(()=>{
    

    downloadCSVFile(convertTbodyToCSV(document.querySelector('#resultat'),false),'resultatClassification.csv',false) // for the client
    downloadCSVFile(convertTbodyToCSV(document.querySelector('#resultat'),true),'Classification.csv',true) // for logFile

})
