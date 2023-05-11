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
    // Empêche la soumission normale du formulaire
    event.preventDefault();
    // Affiche le spinner
    if (confirm('Cette étape peut prendre plusieurs minutes. Êtes-vous sûr de vouloir continuer ?')) {
        $('#spinner-container').show();

        // Envoie la requête Ajax pour traiter le formulaire
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
                // Cache le spinner
                $('.spinner-border').hide();
                $('#spinner-container').hide();
                // Affiche les tables HTML renvoyées
                
                if($('#termes').length){
                    $('#termes').html(data.termes)
                }
            })
            .catch(error => {
                // Cache le spinner
                $('.spinner-border').hide();
                $('#spinner-container').hide();
                // Affiche un message d'erreur
                alert(error.message);
            });
        } else {
            // L'utilisateur a annulé la soumission du formulaire
            alert('La soumission du formulaire a été annulée.');
          }
    });

    

    $('#useTermesForm').on('submit', function (event) {
        console.log("test")
        // Empêche la soumission normale du formulaire
        event.preventDefault();
        // Affiche le spinner
        if (confirm('Cette étape peut prendre plusieurs minutes. Êtes-vous sûr de vouloir continuer ?')) {
            $('#spinner-container').show();
    
            // Envoie la requête Ajax pour traiter le formulaire
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
                    // Cache le spinner
                    $('.spinner-border').hide();
                    $('#spinner-container').hide();
                    // Affiche les tables HTML renvoyées
                    

                    $('#termesSimilaires').html(data.termesSimilaires);

                    
                })
                .catch(error => {
                    // Cache le spinner
                    $('.spinner-border').hide();
                    $('#spinner-container').hide();
                    // Affiche un message d'erreur
                    alert(error.message);
                });
            } else {
                // L'utilisateur a annulé la soumission du formulaire
                alert('La soumission du formulaire a été annulée.');
              }
        });


        $('#useThematiquesForm').on('submit', function (event) {
            console.log("test")
            // Empêche la soumission normale du formulaire
            event.preventDefault();
            // Affiche le spinner
            if (confirm('Cette étape peut prendre plusieurs minutes. Êtes-vous sûr de vouloir continuer ?')) {
                $('#spinner-container').show();
        
                // Envoie la requête Ajax pour traiter le formulaire
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
                        // Cache le spinner
                        $('.spinner-border').hide();
                        $('#spinner-container').hide();
                        // Affiche les tables HTML renvoyées
                        
    
                        $('#thematiques').html(data.thematiques);
    
                        
                    })
                    .catch(error => {
                        // Cache le spinner
                        $('.spinner-border').hide();
                        $('#spinner-container').hide();
                        // Affiche un message d'erreur
                        alert(error.message);
                    });
                } else {
                    // L'utilisateur a annulé la soumission du formulaire
                    alert('La soumission du formulaire a été annulée.');
                  }
            });

// export csv untrained
function exportToCSV() {
    // Vérifier si le tbody contient des lignes
    var tbody = document.querySelector("tbody#termes");
    var rows = tbody.getElementsByTagName("tr");
    if (rows.length === 0) {
      // Aucune ligne trouvée, afficher un message d'erreur ou faire une action alternative
      console.log("Aucun terme trouvé pour exporter.");
      return;
    }
  
    // Créer un tableau pour stocker les données CSV
    var csvData = [];
  
    // Parcourir chaque ligne du tbody
    for (var i = 0; i < rows.length; i++) {
      var rowData = [];
      var columns = rows[i].querySelectorAll("td");
  
      // Parcourir chaque colonne de la ligne, en ignorant le premier td
      for (var j = 1; j < columns.length; j++) {
        var columnData = columns[j].textContent.trim();
        rowData.push(columnData);
      }
  
      // Ajouter la ligne au tableau de données CSV
      csvData.push(rowData);
    }
  
    // Convertir le tableau de données CSV en format CSV
    var csvContent = csvData.map(row => row.join(";")).join("\n");
  
    // Télécharger le fichier CSV
    var fileName = "termes_liste.csv";
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
  exportButton.addEventListener("click", exportToCSV);


 
  
  $("#termes_sim").click(() => {
    const baseUrl = window.location.origin;
    const apiEndpoint = "rechercheSimilariteAPI/";
    
    const apiUrl = new URL(apiEndpoint, baseUrl).href;
    console.log(apiUrl);
    
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        // Traiter les données JSON
        console.log(data)
        const csvContent = convertToCSV(data);
        console.log(csvContent)
         downloadCSV(csvContent, 'termes_similaires.csv');
      })
      .catch(error => {
        // Gérer les erreurs de la requête
        console.error('Erreur :', error);
      });
  });
  

  function convertToCSV(jsonData) {
    const delimiter = ';'; // Délimiteur CSV
    
    const headers = Object.keys(jsonData[0]);
    const rows = jsonData.map(obj => Object.values(obj)[0].join(delimiter));
    
    const csvContent = [
      headers.join(delimiter),
      ...rows
    ].join('\n');
    
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
  