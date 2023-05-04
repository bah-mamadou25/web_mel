(function (){
    var listvalid=[];
    var listsup=[];
    var valAtt=[];

    var cellules=document.getElementsByClassName('validation');
    for (var i of cellules)
    {
        i.addEventListener('click',function(e){ 
            console.log('un click');
            if(this.classList.contains("selectionne")){
                this.classList.remove("selectionne");
                this.parentNode.style.backgroundColor="#ffffff"
            }
            else{
                this.classList.add("selectionne");
                this.parentNode.style.backgroundColor="#007bff"
            }
        },false);
    }
    var valider= document.getElementById('valider');
    valider.addEventListener('click',function(){
            
    var selec=document.getElementsByClassName('selectionne');
    console.log(selec);
    for (var i of selec)
    {
        listvalid.push(i.innerHTML);
       
    }
    while (selec.length > 0) {
        selec[0].parentNode.parentNode.removeChild(selec[0].parentNode);
    }
    
    console.log(listvalid);
    },false);
    var sup= document.getElementById('supprimer');
    sup.addEventListener('click',function(){
            
    var cellulesSup=document.getElementsByClassName('selectionne');
    for (var i of cellulesSup)
    {
        listsup.push(i.innerHTML);
    }
    while (cellulesSup.length > 0) {
        cellulesSup[0].parentNode.parentNode.removeChild(cellulesSup[0].parentNode);
    }
    
    console.log(listsup);
    },false);

    // Fonction pour convertir le tableau en une chaîne CSV
    function convertToCSV(arr) {
        var csv = "";
        for (var i of arr) {
          csv += i+ "\n";
        }
        return csv;
      }
  // Fonction pour télécharger le fichier CSV
function downloadCSV(csv, filename) {
    var csvFile = new Blob([csv], { type: "text/csv" });
    var downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    downloadLink.parentNode.removeChild(downloadLink);
  }

  var Telecharger_valider= document.getElementById('Tvalider');
  Telecharger_valider.addEventListener('click',function(){
    chaineCsv=convertToCSV(listvalid);
    downloadCSV(chaineCsv,'entities.csv');
  },false);

  var Telecharger_Nvalider= document.getElementById('TNvalider');
  Telecharger_Nvalider.addEventListener('click',function(){
    for(var i of cellules)
        valAtt.push(i.innerHTML);
    chaineCsv=convertToCSV(valAtt);
    console.log(valAtt);
    downloadCSV(chaineCsv,'enAttenteDeValidation.csv');
  },false);

  
    

}
)();