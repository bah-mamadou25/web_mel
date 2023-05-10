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
      for (let i of columns) {
        if(!i.querySelector("svg")&& i!==columns[0])
        {
          const columnData = i.textContent.trim();
        rowData.push(columnData);

        }
        
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
                    'elements_attentes.csv');
  });
  
  /**
   * Écouteur d'événement pour le bouton de téléchargement associé à l'élément avec l'id 'valider'.
   * Convertit le contenu du tbody correspondant en CSV et télécharge le fichier.
   */
  $(".download-val").click(function() {
    downloadCSVFile(convertTbodyToCSV(document.querySelector('#valider tbody')),
                    'elements_validés.csv');
  });
  
  /**
   * Écouteur d'événement pour le bouton de téléchargement associé à l'élément avec l'id 'supprimer'.
   * Convertit le contenu du tbody correspondant en CSV et télécharge le fichier.
   */
  $(".download-sup").click(function() {
    downloadCSVFile(convertTbodyToCSV(document.querySelector('#supprimer tbody')),
                    'elements_supprimés.csv');
  });
  

  function ajoutActions(idTable,contentTd1,contentTd2){
    var tableBody = document.getElementById(idTable).getElementsByTagName("tbody")[0];

// boucle à travers chaque ligne
for (var i = 0; i < tableBody.rows.length; i++) {
  // créer deux nouvelles cellules
  var newCell1 = document.createElement("td");
  newCell1.innerHTML = contentTd1
  tableBody.rows[i].appendChild(newCell1);
  if (contentTd2!=""){
    var newCell2 = document.createElement("td");
    newCell2.innerHTML = contentTd2
    tableBody.rows[i].appendChild(newCell2);
  }
   
  
}
}


/**
 * Construit un élément <tr> contenant des <td> avec le contenu du terme,
 * ainsi que deux autres <td> avec les contenus spécifiés.
 * @param {Array} terme - Les données du terme à afficher dans les <td> du <tr>.
 * @param {string} contentTd1 - Le contenu du premier <td> à ajouter.
 * @param {string} contentTd2 - Le contenu du deuxième <td> à ajouter.
 * @returns {HTMLElement} - L'élément <tr> créé.
 */




function ajoutActionToRestaureTerme(terme, contentTd1, contentTd2) {
  // Création de l'élément <tr>
  var tr = document.createElement('tr');

  // Boucle sur les données du terme pour créer les <td>
  terme.forEach(function (data) {
    // Création d'un <td> pour chaque donnée du terme
    var td = document.createElement('td');
    td.textContent = data;
    tr.appendChild(td); // Ajout du <td> au <tr>
  });

  // Création du premier <td> supplémentaire
  var td1 = document.createElement('td');
  td1.innerHTML = contentTd1;
  tr.appendChild(td1); // Ajout du premier <td> supplémentaire au <tr>
  tr.querySelector('td:last-child svg').style.cursor="pointer";
  tr.querySelector('td:last-child svg').addEventListener('click',supEvent)





  
  // Création du deuxième <td> supplémentaire
  var td2 = document.createElement('td');
  td2.innerHTML = contentTd2;
  tr.appendChild(td2); // Ajout du deuxième <td> supplémentaire au <tr>
  tr.querySelector('td:last-child svg').style.cursor="pointer";
  tr.querySelector('td:last-child svg').addEventListener('click',validEvent)
  return tr;
}

/**
 * Génère un élément tr avec des éléments td contenant le contenu du tableau et
 * le dernier élément td contenant la chaîne de caractères en tant qu'innerHTML.
 *
 * @param {Array} values - Le tableau de valeurs à placer dans les éléments td.
 * @param {string} htmlString - La chaîne de caractères à utiliser pour le dernier élément td.
 * @returns {HTMLElement} - L'élément tr généré avec les éléments td correspondants.
 */
function createTableRowWithHTMLString(values, htmlString) {
  const tr = document.createElement('tr');

  // boucle sur les valeurs et crée des éléments td pour chacune
  for (const value of values) {
    const td = document.createElement('td');
    td.textContent = value;
    tr.appendChild(td);
  }

  // crée un dernier élément td avec la chaîne de caractères en tant qu'innerHTML
  const lastTD = document.createElement('td');
  lastTD.innerHTML = htmlString;
  tr.appendChild(lastTD);

  return tr;
}

function getFirstTDsContent(tr, i) {
  const tds = tr.querySelectorAll('td');
  const content = [];

  // boucle sur les `i` premiers éléments `td`
  for (let j = 0; j < i && j < tds.length; j++) {
    content.push(tds[j].textContent);
  }

  return content;
}

function RestaureElement(event) {

  var toRestaure = event.target.parentNode.parentNode;
  if (toRestaure.tagName != 'TR') {
    // si propagation sur la balise path interieur de celle de svg
    toRestaure=toRestaure.parentNode
  }
  toRestaure.parentNode.removeChild(toRestaure)

  var termeContent=getFirstTDsContent(toRestaure,colDon)


  toRestaure=ajoutActionToRestaureTerme(termeContent,svgSup,svgValid)

  tableA.insertAdjacentElement('afterbegin',toRestaure)

}

$(document).ready(function() {
  // Afficher la div "attente" et masquer les autres divs au chargement de la page
  $("#attente").show();
  $("#valider").hide();
  $("#supprimer").hide();
  console.log($(".toggle-print"));

  // Ajouter un gestionnaire d'événements pour les boutons radio
  $(".toggle-print").click(function() {
    var id = $(this).attr("id");
    if (id == "buttonA") {
      $("#attente").show();
      $("#valider").hide();
      $("#supprimer").hide();
    } else if (id == "buttonV") {
      $("#attente").hide();
      $("#valider").show();
      $("#supprimer").hide();
    } else if (id == "buttonS") {
      $("#attente").hide();
      $("#valider").hide();
      $("#supprimer").show();
    }
  });
});


var supEvent = function (event) {
var row = event.target.parentNode.parentNode;
if (row.tagName != 'TR') {
  // si propagation sur la balise path interieur de celle de svg
  row = row.parentNode;
}

row.parentNode.removeChild(row);
toadd = getFirstTDsContent(row, colDon);
toappend = createTableRowWithHTMLString(toadd, svgRest);
console.log(toappend.querySelector('td:last-child svg'));
tableS.append(toappend);

var deleteIcon = toappend.querySelector('td:last-child svg');
deleteIcon.style.cursor = 'pointer';

deleteIcon.addEventListener('click', function (el) {
  RestaureElement(el);
});
};

var validEvent = function(event) {
var row = event.target.parentNode.parentNode;
if (row.tagName != 'TR') {
  // si propagation sur la balise path intérieur de celle de svg
  row = row.parentNode;
}

row.parentNode.removeChild(row);
var toadd = getFirstTDsContent(row, colDon);
var toappend = createTableRowWithHTMLString(toadd, svgRest);
tableV.append(toappend);

var validIcon = document.querySelector('#valider tr:last-child td:last-child svg');
validIcon.style.cursor = 'pointer';

validIcon.addEventListener('click', function(el) {
  RestaureElement(el);
});
};