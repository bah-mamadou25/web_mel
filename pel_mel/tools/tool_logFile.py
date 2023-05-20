import csv
from datetime import datetime




def ajouter_ligne_csv(chemin_fichier, valeurs):
    """
    Ajoute une ligne avec les valeurs spécifiées au fichier CSV.

    :param chemin_fichier: Chemin du fichier CSV.
    :type chemin_fichier: str
    :param valeurs: Tableau des valeurs à ajouter.
    :type valeurs: list
    """

    # Ouvrir le fichier CSV en mode append
    with open(chemin_fichier, 'a', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerow(valeurs)











def count_modified_values(csv1_content, csv2_content):
    """
    Compte le nombre de valeurs modifiées entre deux fichiers CSV.

    :param csv1_content: Contenu du premier fichier CSV.
    :type csv1_content: str
    :param csv2_content: Contenu du deuxième fichier CSV.
    :type csv2_content: str
    :return: Nombre de valeurs modifiées.
    :rtype: [int,int,...]
    """
    count = 0
    
    csv1_lines = csv1_content.strip().split('\n')
    csv2_lines = csv2_content.strip().split('\n')

    nb_lines=len(csv1_lines)
    validés=nb_lines
   
    
    nb_facettes_total=(len(csv1_lines[0].split(';'))-2)*nb_lines
    if nb_lines != len(csv2_lines):
        raise ValueError("Les deux fichiers CSV n'ont pas le même nombre de lignes.")

    
    for csv1_line, csv2_line in zip(csv1_lines, csv2_lines):
        csv1_fields = csv1_line.split(';')
        csv2_fields = csv2_line.split(';')
        if len(csv1_fields) != len(csv2_fields):
            raise ValueError("Les deux fichiers CSV n'ont pas le même nombre de champs à la ligne correspondante.")

        for csv1_field, csv2_field in zip(csv1_fields, csv2_fields):
            
                if csv2_field=='notchecked':
                    validés-=1
                else:
                    if csv1_field != csv2_field:
                        count += 1

    return [get_current_datetime(),count,nb_facettes_total,validés,nb_lines]









def generer_contenu_champs_csv(csv_file, nb):
    """
    Génère le contenu des nb premiers champs de chaque ligne d'un fichier CSV en ajoutant checked pour le log.

    :param csv_file: Chemin du fichier CSV.
    :type csv_file: str
    :param nb: Nombre de premiers champs à prendre en compte.
    :type nb: int
    :return: Contenu des nb premiers champs de chaque ligne.
    :rtype: str
    """

   
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        lines = list(reader)

    # Rajoute 'checked' pour nous permettre de savoir le nb d'éléments sélectionnés
    contenu_champs = [';'.join(line[:nb]) for line in lines[1:]]
    contenu_final = '\n'.join([champ + ';checked' for champ in contenu_champs])

    return contenu_final







def nb_champs(content):
    lines = content.strip().split('\n')  # Séparer les lignes du contenu SVG
    first_line = lines[0].strip()  # Récupérer la première ligne
    
    # Compter le nombre de champs dans la première ligne
    count = first_line.count(';')

    
    return count







def addToLogfile(new_result,old_result_path):
    old_result=generer_contenu_champs_csv(old_result_path,nb_champs(new_result))
    print(old_result)
    stats=count_modified_values(old_result,new_result)
    ajouter_ligne_csv('classificationStats.csv',stats)
    
    
    
def get_current_datetime():
    now = datetime.now() 
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  
    return formatted_datetime