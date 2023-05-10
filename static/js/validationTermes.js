


function filterJsonByScore(jsonData, minScore, maxScore) {
  // Convertir la chaîne JSON en objet JavaScript
  const data = JSON.parse(jsonData);

  // Filtrer les éléments en fonction du score
  const filteredData = Object.entries(data).filter(([key, value]) => {
    const score = parseFloat(value[0].split(';')[1]);
    return score >= minScore && score <= maxScore;
  });

  // Convertir les éléments filtrés en objet JavaScript
  const filteredJson = Object.fromEntries(filteredData);

  // Retourner les éléments filtrés en format JSON
  return JSON.stringify(filteredJson);
}











var colDon=4;

// icone svg
var svgValid='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" class="bi bi-check2-circle" viewBox="0 0 16 16"><path d="M2.5 8a5.5 5.5 0 0 1 8.25-4.764.5.5 0 0 0 .5-.866A6.5 6.5 0 1 0 14.5 8a.5.5 0 0 0-1 0 5.5 5.5 0 1 1-11 0z"/><path d="M15.354 3.354a.5.5 0 0 0-.708-.708L8 9.293 5.354 6.646a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l7-7z"/></svg>';
var svgSup='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-x-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/></svg>';
var svgRest='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="blue" class="bi bi-reply-fill" viewBox="0 0 16 16"><path d="M5.921 11.9 1.353 8.62a.719.719 0 0 1 0-1.238L5.921 4.1A.716.716 0 0 1 7 4.719V6c1.5 0 6 0 7 8-2.5-4.5-7-4-7-4v1.281c0 .56-.606.898-1.079.62z"/></svg>'

//tbody des tableau
const tableA = document.querySelector('#attente tbody');
const tableV = document.querySelector('#valider tbody');
const tableS = document.querySelector('#supprimer tbody');


//ajout icone
ajoutActions("attente",svgSup,svgValid);
ajoutActions("supprimer",svgRest,"");



S=document.querySelectorAll("#attente tbody td:nth-child(5) svg");
V=document.querySelectorAll("#attente tbody td:last-child svg");
R=document.querySelectorAll("#valider tbody td:last-child svg, #supprimer tbody td:last-child svg ");


// Gestion event si nous cliquons sur l'icone supprimer
S.forEach(function (e) {
  e.style.cursor = 'pointer';
  e.addEventListener('click', supEvent);
});

// gestion event si nous clickons sur l'icone valider
V.forEach((e)=>{
    e.style.cursor='pointer'
    e.addEventListener('click',validEvent);

})


