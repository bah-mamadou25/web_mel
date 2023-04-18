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
  