

function filterJsonByScore(data, minScore, maxScore) {
    // Filtrer les éléments en fonction du score
    const filteredData = data.filter((entry) => {
      const value = Object.values(entry)[0][0];
      const scoreMatch = value.match(/[-+]?[0-9]*\.?[0-9]+/);
      if (scoreMatch) {
        const score = parseFloat(scoreMatch[0]);
        return score >= minScore && score <= maxScore;
      }
      return false;
    });
  
    return filteredData;
  }


  function downloadFilteredTerme(data) {
    // Créer le contenu du fichier CSV
    let csvContent = "data:text/csv;charset=utf-8,";
  
    // Ajouter chaque ligne au contenu CSV
    data.forEach((entry) => {
      const values = Object.values(entry)[0];
      const csvLine = values.map((value) => `"${value}"`).join(";");
      csvContent += csvLine + "\r\n";
    });
  
    // Créer un lien de téléchargement
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "termes_filtered.csv");
  
    // Ajouter le lien à la page et déclencher le téléchargement
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }