
/**
* Attache un gestionnaire d'événement à la soumission du formulaire avec l'ID "my-form".
* Empêche la soumission normale du formulaire, affiche un spinner, envoie une requête Ajax
* pour traiter le formulaire, affiche le résultat et cache le spinner. En cas d'erreur, affiche
* un message d'erreur.
*/

$('#my-form').on('submit', function (event) {
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
                }else{
                    $('#table_personnes').html(data.table_personnes);
                    $('#table_organisations').html(data.table_organisations);
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

