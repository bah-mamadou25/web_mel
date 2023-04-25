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