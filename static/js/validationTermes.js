var svgValid='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" class="bi bi-check2-circle" viewBox="0 0 16 16"><path d="M2.5 8a5.5 5.5 0 0 1 8.25-4.764.5.5 0 0 0 .5-.866A6.5 6.5 0 1 0 14.5 8a.5.5 0 0 0-1 0 5.5 5.5 0 1 1-11 0z"/><path d="M15.354 3.354a.5.5 0 0 0-.708-.708L8 9.293 5.354 6.646a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l7-7z"/></svg>';
var svgSup='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-x-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/></svg>';
var svgRestaure='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="blue" class="bi bi-reply-fill" viewBox="0 0 16 16"><path d="M5.921 11.9 1.353 8.62a.719.719 0 0 1 0-1.238L5.921 4.1A.716.716 0 0 1 7 4.719V6c1.5 0 6 0 7 8-2.5-4.5-7-4-7-4v1.281c0 .56-.606.898-1.079.62z"/></svg>'


const tableA = document.querySelector('#attente tbody');
const tableV = document.querySelector('#valider tbody');
const tableS = document.querySelector('#supprimer tbody');



ajoutActions("attente",svgSup,svgValid);
ajoutActions("supprimer",svgRestaure,"");



S=document.querySelectorAll("#attente tbody td:nth-child(5) svg");
V=document.querySelectorAll("#attente tbody td:last-child svg");

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
















S.forEach((e)=>{
    e.style.cursor="pointer" 
    e.addEventListener("click",(event)=>{
       

    var row = event.target.parentNode.parentNode;
    if (row.tagName != 'TR') {
    // si propagation sur la balise path interieur de celle de svg
    row=row.parentNode
    }

    row.parentNode.removeChild(row)
    toadd=getFirstTDsContent(row,4)
    toappend=createTableRowWithHTMLString(toadd,svgRestaure)
    tableS.append(toappend)
    
})
})

V.forEach((e)=>{
    e.style.cursor="pointer"
    e.addEventListener("click",(event)=>{
       

     var row = event.target.parentNode.parentNode;
     if (row.tagName != 'TR') {
       // si propagation sur la balise path in terieur de celle de svg
       row=row.parentNode
     }

     row.parentNode.removeChild(row)
     toadd=getFirstTDsContent(row,4)
     toappend=createTableRowWithHTMLString(toadd,svgRestaure)
     tableV.append(toappend)
    })
})




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
