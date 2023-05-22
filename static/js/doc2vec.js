$('.spinner-border').hide();
$('#spinner-container').hide();

// Fonction pour vérifier si le tbody a au moins une ligne
function checkRowCount() {
    var tbody = document.getElementById("resultat");
    return tbody.getElementsByTagName("tr").length > 0;
  }


  function getSelectedRadioId() {

    var radiosDiv = document.getElementById('radios-choice');
  
  
    var radioInputs = radiosDiv.querySelectorAll('input[type="radio"][name="facette"]');
  
   
    for (var i = 0; i < radioInputs.length; i++) {
      if (radioInputs[i].checked) {
       
        return radioInputs[i].id;
      }
    }

    return null;
  }

function modifTd(td){
  resultat=getSelectedRadioId()
  if(resultat){
      td.innerText=resultat

  }
}














  const input1 = document.getElementById('thematique2');
  const input2 = document.getElementById('thematique3');

  input2.disabled = true;
  input1.addEventListener('change', () => {
    if (input1.files.length > 0) {
      input2.disabled = false; 
    } else {
      input2.disabled = true; 
    }
  });
  
  
  
  // Timer pour vérifier toutes les 2 secondes
  var timer = setInterval(function() {
    console.log("boucle")
    if (checkRowCount()) {
  
      clearInterval(timer);
   


      editFacette();

      $('.spinner-border').show();
      $('#spinner-container').show();
      // 

      setEventVoir();
      document.getElementById("validationV").addEventListener("click", onClicValides);
      document.getElementById("validationT").addEventListener("click", onClicTous);
      document.getElementById("validationN").addEventListener("click", onClicNonValides);
      modifDropDownByLevel('#liste-thematiques','1:',1);
      modifDropDownByLevel('#liste-thematiques','2:',2);
      modifDropDownByLevel('#liste-thematiques','3:',3);

      if(isEmptyColumn('#resultat',2)){
        document.querySelector('th:nth-child(3)').style.display='none';
        hideTdsByIndex('#resultat',2)
        
      }

      if(isEmptyColumn('#resultat',3)){
        document.querySelector('th:nth-child(4)').style.display='none';
        hideTdsByIndex('#resultat',3)
        
      }

      $('.spinner-border').hide();
      $('#spinner-container').hide();

      document.querySelector('#telecharger').removeAttribute('disabled')


      
    } 
  }, 2000); 


function editFacette(){

      
      var tbody = document.getElementById("resultat");
  
     
      var rows = tbody.getElementsByTagName("tr");
      for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        for (var j = 1; j < 4; j++) {
          var cell = cells[j];
  
          // Ajouter un événement de clic à chaque td
          cell.addEventListener("click", function() {
            var text = this.textContent;
            var position=this.cellIndex

            
            var rightFacette=getMatchingLiInnerText('#liste-thematiques',position+':')
            console.log(rightFacette)

            radiosLi=''

            for(e of rightFacette){
              radiosLi+='<div>'
              e=e.split(':')[1];
              if(e==text){
                radiosLi+='<input type="radio" name="facette" id="'+e+'" checked /> '+e+'<br>'
              }else{
                radiosLi+='<input type="radio" name="facette" id="'+e+'"  />'+e+'<br>'

              }
              radiosLi+='</div>'
            }

            document.querySelector('#closebtn').addEventListener('click',(e)=>{
              divModal.parentNode.style.display="none"
              modifTd(this)
            })

            divModal=document.querySelector("#radios-choice ")
            divModal.parentNode.style.display="block"
            divModal.innerHTML=radiosLi;
            console.log(radiosLi)

          });
        }
      }
}



  function voirDoc(jsonData){
        var text=jsonData["content"]
        console.log(text)
        
        const data_=text.split('##split##')
        const repertoire=data_[0]
        text=data_[1].split('\n')
        var text_html=''
        
        data_.forEach((e)=>{
            text_html='<span>'+e+'</span><br>'
        })

        document.querySelector('#repertoire').innerHTML=repertoire
        document.querySelector('#docContent').innerHTML=text_html

        // console.log(repertoire)
        // console.log(text_html)
    }


function setEventVoir(){
    // Sélectionner tous les liens dans les derniers <td> de chaque ligne du tbody
var tbody = document.getElementById("resultat");
var links = tbody.querySelectorAll("tr td:last-child a");

// Ajouter un gestionnaire d'événements click à chaque lien
links.forEach(function(link) {
  link.addEventListener("click", function(event) {
    event.preventDefault();

    var url = link.getAttribute("href");

    fetch(url)
      .then(function(response) {
        if (!response.ok) {
          throw new Error("Erreur lors de la requête");
        }
        return response.json();
      })
      .then(function(data) {
        
        console.log(data);
        voirDoc(data);

        document.querySelector('#voirdoc').style.display="block"


      })
      .catch(function(error) {
        console.log(error);
      });


  });
});

}
  





// Sélectionner le bouton de fermeture
var closeButton = document.querySelector("#voirdoc .close");

// Ajouter un gestionnaire d'événements au bouton de fermeture
closeButton.addEventListener("click", function() {
  // Sélectionner la div "voirdoc"
  var voirdocDiv = document.getElementById("voirdoc");
  
  // Masquer la div en définissant la propriété "display" sur "none"
  voirdocDiv.style.display = "none";

});



function getThematiquebyLevel(tbodyId,tdNum) {
    tds=document.querySelectorAll(tbodyId +' '+'tr td:nth-child('+tdNum+')' )
    var resultat=[];
    tds.forEach((td)=>{
        if(!resultat.includes(td.innerText)){
        resultat.push(td.innerText);
            
        }
    })

    return resultat;
}

function modifDropDownByLevel(tbodyId,startwith,level){
    var levelIds=["#ulLevel1","#ulLevel2","#ulLevel3"]
    var toAdd=getMatchingLiInnerText(tbodyId,startwith)  // car niveau se situe à td+1

    for (const l of toAdd) {
        
        document.querySelector(levelIds[level-1]).innerHTML+='<li class="dropdown-item" >'+l.split(':')[1]+'</li>';
    }
}






////////////FILTRE 














// Fonction pour masquer les lignes qui ne correspondent pas au critère
function masquerLignesNonValidees() {
   
    var lignes = document.querySelectorAll("#resultat tr");
  
  
    lignes.forEach(function (ligne) {
    
      var cinquiemeTd = ligne.querySelector("td:nth-of-type(5)");
  
      var checkbox = cinquiemeTd.querySelector("input[type='checkbox']");
  
      if (!checkbox.checked) {
        ligne.style.display = "none";
      }else{
        ligne.style.display =""
      }
    });
  }

  function masquerLignesValidees() {
   
    var lignes = document.querySelectorAll("#resultat tr");
  
  
    lignes.forEach(function (ligne) {
    
      var cinquiemeTd = ligne.querySelector("td:nth-of-type(5)");
  
      var checkbox = cinquiemeTd.querySelector("input[type='checkbox']");
  
      if (checkbox.checked) {
        ligne.style.display = "none";
      }else{
        ligne.style.display =""
      }
    });
  }




  
  function afficherToutesLesLignes() {
    var lignes = document.querySelectorAll("#resultat tr");
  
    lignes.forEach(function (ligne) {
      ligne.style.display = "";
    });
  }
  
  function onClicValides() {
    masquerLignesNonValidees();
    document.querySelector('#appliedV').innerHTML='[Validé.s]'
  }
  
  function onClicTous() {
    afficherToutesLesLignes();
    document.querySelector('#appliedV').innerHTML='[Tous]'

  }
  

function onClicNonValides() {
    masquerLignesValidees();
    document.querySelector('#appliedV').innerHTML='[Non validé.s]'

}


