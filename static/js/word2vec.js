$('#download-them').hide();
$('#download-sim').hide();


$(document).ready(function() {
    $('#train').click(function() {
        $('#trainDiv').show();
        $('#useDiv').hide();
      })
      $('#use').click(function() {
        $('#useDiv').show();
        $('#trainDiv').hide();
      })

      $('#terme').click(function() {
        $('#termeDiv').show();
        $('#thematiqueDiv').hide();
      })
      $('#thematique').click(function() {
        $('#thematiqueDiv').show();
        $('#termeDiv').hide();
      })

  });
  

/**
* Attache un gestionnaire d'événement à la soumission du formulaire avec l'ID "my-form".
* Empêche la soumission normale du formulaire, affiche un spinner, envoie une requête Ajax
* pour traiter le formulaire, affiche le résultat et cache le spinner. En cas d'erreur, affiche
* un message d'erreur.
*/

$('#my-trainForm').on('submit', function (event) {
    event.preventDefault();
    if (confirm('Cette étape peut prendre plusieurs minutes. Êtes-vous sûr de vouloir continuer ?')) {
        $('#spinner-container').show();

        fetch($(this).attr('action'), {
            method: $(this).attr('method'),
            body: new FormData(this),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Une erreur s\'est produite.');
                }
                return response.json();
            })
            .then(data => {
                $('.spinner-border').hide();
                $('#spinner-container').hide();
                
                if($('#termes').length){
                    $('#termes').html(data.termes)
                }
            })
            .catch(error => {
                $('.spinner-border').hide();
                $('#spinner-container').hide();
                alert(error.message);
            });
        } else {
            alert('La soumission du formulaire a été annulée.');
          }
    });

    

    $('#useTermesForm').on('submit', function (event) {
        console.log("test")
        event.preventDefault();
        if (confirm('Cette étape peut prendre plusieurs minutes. Êtes-vous sûr de vouloir continuer ?')) {
            $('#spinner-container').show();
    
            fetch($(this).attr('action'), {
                method: $(this).attr('method'),
                body: new FormData(this),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Une erreur s\'est produite.');
                    }
                    return response.json();
                })
                .then(data => {
                    $('.spinner-border').hide();
                    $('#spinner-container').hide();
                    

                    $('#termesSimilaires').html(data.termesSimilaires);
                    $('#termesSimilaires tr td:last-child').click((event) => {
                      const tdElement = event.target;
                      const currentValue = tdElement.innerText;
                    
                      const confirmation = confirm('Voulez-vous modifier ce contenu : ' + currentValue + ' ?');
                      if (confirmation) {
                        const newValue = prompt('Modifier le contenu :', currentValue);
                        if (newValue !== null) {
                          tdElement.innerText = newValue;
                        }
                      }

                      $('#download-sim').show()
                      $('#download-sim').click((event)=>{
                        exportToCSV('#termesSimilaires','termes_similaires.csv')
                      })
                    });
                })
                .catch(error => {
                    $('.spinner-border').hide();
                    $('#spinner-container').hide();
                    alert(error.message);
                });
            } else {
                alert('La soumission du formulaire a été annulée.');
              }
        });


        $('#useThematiquesForm').on('submit', function (event) {
            console.log("test")
            event.preventDefault();
            if (confirm('Cette étape peut prendre plusieurs minutes. Êtes-vous sûr de vouloir continuer ?')) {
                $('#spinner-container').show();
        
                fetch($(this).attr('action'), {
                    method: $(this).attr('method'),
                    body: new FormData(this),
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Une erreur s\'est produite.');
                        }
                        return response.json();
                    })
                    .then(data => {
                        $('.spinner-border').hide();
                        $('#spinner-container').hide();
                        
    
                        $('#thematiques').html(data.thematiques);

                        $('#thematiques tr td:last-child').click((event) => {
                          const tdElement = event.target;
                          const currentValue = tdElement.innerText;
                        
                          const confirmation = confirm('Voulez-vous modifier ce contenu : ' + currentValue + ' ?');
                          if (confirmation) {
                            const newValue = prompt('Modifier le contenu :', currentValue);
                            if (newValue !== null) {
                              tdElement.innerText = newValue;
                            }
                          }
    
                          $('#download-them').show()
                          $('#download-them').click(()=>{
                            exportToCSV('#thematiques','nuageDeMotsViaSearch.csv')
                          })
                        });
    
                        
                    })
                    .catch(error => {
                        // Cache le spinner
                        $('.spinner-border').hide();
                        $('#spinner-container').hide();
                        // Affiche un message d'erreur
                        alert(error.message);
                    });
                } else {
                    alert('La soumission du formulaire a été annulée.');
                  }
            });

// export csv untrained
function exportToCSV(selector,fileName) {
    // Vérifier si le tbody contient des lignes
    var tbody = document.querySelector(selector);
    var rows = tbody.getElementsByTagName("tr");
    if (rows.length === 0) {
      // Aucune ligne trouvée, afficher un message d'erreur ou faire une action alternative
      console.log("Aucun terme trouvé pour exporter.");
      return;
    }
  
    // Créer un tableau pour stocker les données CSV
    var csvData = [];
  

    for (var i = 0; i < rows.length; i++) {
      var rowData = [];
      var columns = rows[i].querySelectorAll("td");

      for (var j = 1; j < columns.length; j++) {
        var columnData = columns[j].textContent.trim();
        rowData.push(columnData);
      }

      csvData.push(rowData);
    }
  
    var csvContent = csvData.map(row => row.join(";")).join("\n");
  
    // Télécharger le fichier CSV
    var link = document.createElement("a");
    link.setAttribute("href", "data:text/csv;charset=utf-8," + encodeURIComponent(csvContent));
    link.setAttribute("download", fileName);
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  
  // Ajouter un écouteur d'événement au bouton "export"
  var exportButton = document.getElementById("export");
  exportButton.addEventListener("click",()=>{
    exportToCSV('#termes','liste_termes.csv')
  } );


 
  
  $("#termes_sim").click(() => {

    var res=confirm("Un fichier csv sera téléchargé, les termes similaires seront sur la même ligne")

    if(!res) return;
    const baseUrl = window.location.origin;
    const apiEndpoint = "rechercheSimilariteAPI/";
    
    const apiUrl = new URL(apiEndpoint, baseUrl).href;
    console.log(apiUrl);
    
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
       
        console.log(data)
        const csvContent = convertToCSV(data);
        console.log(csvContent)
         downloadCSV(csvContent, 'termes_similaires.csv');
      })
      .catch(error => {
        
        console.error('Erreur :', error);
      });
  });
  

  function convertToCSV(jsonData) {
    const delimiter = ';'; // Délimiteur CSV
  
    const rows = jsonData.map(obj => Object.values(obj)[0].join(delimiter));
  
    const csvContent = rows.join('\n');
  
    return csvContent;
  }
  

  function downloadCSV(csvContent, fileName) {
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const blobUrl = URL.createObjectURL(blob);
    
    const downloadLink = document.createElement('a');
    downloadLink.href = blobUrl;
    downloadLink.download = fileName;
    
    downloadLink.click();
    
    URL.revokeObjectURL(blobUrl);
  }
  
