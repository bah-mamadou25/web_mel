import os,csv
import subprocess
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from .termsExtraction import *




"""
création de fichier de configuration d'entrée à l'extracteur de termes
exécution de l'extracteur
renvoie True si l'extracteur a donné un fichier contenant les termes en sortie
False sinon
"""
def termsExtraction(corpus_path, termsExtracted_path, STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX):
    print("Création de fichier de configuartion d'entrée à l'extrateur de termes...")
    fichier_config = open("PLDAC-master/fichier_config.cfg", "w")
    fichier_config.write("CORPUSPATH = " + corpus_path)
    fichier_config.write("\n")
    fichier_config.write("OUTPUTPATH = " + termsExtracted_path)
    fichier_config.write("\n")
    fichier_config.write("STEM = " + STEM)
    fichier_config.write("\n")
    fichier_config.write("METHODEEXTRACTION = POSTAG")
    fichier_config.write("\n")
    fichier_config.write("LONGUEURMIN = " + LONGUEURMIN)
    fichier_config.write("\n")
    fichier_config.write("LONGUEURMAX = " + LONGUEURMAX)
    fichier_config.write("\n")
    fichier_config.write("SEUILNBOCCMIN = 0")
    fichier_config.write("\n")
    fichier_config.write("FORMULEAGREGATION = MAX")
    fichier_config.write("\n")
    fichier_config.write("METHODESCORING = " + METODE_SCORING)
    fichier_config.write("\n")
    fichier_config.write("CVALUE = True")
    fichier_config.close()

    print("Extraction des termes...")

    process = subprocess.Popen(["python3", "PLDAC-master/extractionTerme.py", "PLDAC-master/fichier_config.cfg"])
    process.wait()
    print("Fin d'exécution de l'extracteur de termes !")
    if os.path.exists(termsExtracted_path):
        return True
    else:
        return False
    

def terms_extraction(corpus_path, termsExtracted_path, STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX):
    number_of_sentences = get_number_of_sentences(corpus_path)
    if number_of_sentences < 12050:
        res = termsExtraction(corpus_path, termsExtracted_path, STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX)
        # si l'extracteur a donné un fichier de termes en sortie
        if res:
            terms_list = retreiveTerms(termsExtracted_path)
            terms_list_cleaned = cleanUpTerms(terms_list)
            fw = open(termsExtracted_path, "w", encoding="UTF-8")
            for i in terms_list_cleaned:
                fw.write(str(i.term).strip()+";"+str(i.score).strip()+";"+str(i.source).strip())
                fw.write("\n")
            fw.close()
            return terms_list_cleaned
        else:
            return False
    else:
        # le fichier est très volumineux, il faut le découper en plusieurs fichiers et renvoyer
        # un message d'erreur à l'interface
        split_list_of_phrases(corpus_path, STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX)
        return 'too_bulky'

def merge_files_list(terms_files_list):
    merge_files(terms_files_list)
    pathTo, FileName = os.path.split(terms_files_list[0])
    if os.path.isfile(str(pathTo) + '/liste_termes_fusionnée.csv'):
        return True
    else:
        return False

def automatic_terms_validation(terms_list, terms_reference_list_paths):
    return automaticTermValidation(terms_list, terms_reference_list_paths)


def fileToList(file_path):
    return file_to_list(file_path)

def get_terms_sources(terms_file_path):
    return getTermsSources(terms_file_path)

def split_list_of_phrases(corpus_path, STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX):
    """
    Permet de diviser une longue liste de phrases sur plusieurs listes
    :param corpus_path : chemin vers le corpus
    """
    dir=str(os.path.dirname(corpus_path))[2:]
    parent_dir=str(os.path.dirname(dir))
    print('----------------------')
    print(dir)
    print(parent_dir)
    print('----------------------')
    create_dir(dir+'/bulky')

    os.system('split -l 12000 ' + corpus_path + ' '+dir+'/bulky/')
    for file_name in os.listdir(dir+'/bulky'):
        print(file_name)
        # Exécution de la fonction sur chaque nom de fichier
        terms_extraction(dir+'/bulky/'+file_name, parent_dir+'/workspace/termes/'+file_name+'_termes.csv', STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX)
        
        
def remove_duplicates_and_replace_file(filepath):
    """
    Cette fonction supprime les doublons dans un fichier CSV en calculant la moyenne
    des valeurs du deuxième champ pour les doublons et remplace le fichier traité
    par le fichier nettoyé.
    :param filepath: Le chemin complet vers le fichier CSV à traiter
    """
    data = {}
    with open(filepath, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            key = row[0]
            value = float(row[1])
            if key in data:
                data[key][0] += value
                data[key][1] += 1
            else:
                data[key] = [value, 1]

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for key, value in data.items():
<<<<<<< HEAD
            writer.writerow([key, round(value[0] / value[1], 4), "-"])
=======
            writer.writerow([key, round(value[0] / value[1], 2), "-"])
>>>>>>> f4740638c725dbf2958098ade5037a177479bbfa

    print("Fichier nettoyé : " + filepath)
    
    
def csv_to_json(csv_file_path):
    # Lecture du fichier CSV
    with open(csv_file_path, 'r') as csv_file:
        csv_data = csv.reader(csv_file)

        # Conversion du contenu CSV en format JSON
        json_data = []
        for line_number, row in enumerate(csv_data, start=1):
            json_data.append({str(line_number): row})
    print(json_data)
    # Renvoi de la réponse JSON
<<<<<<< HEAD
    return json_data


def filter_from_csv_termes(input_file_path, reference_file_path, output_file_path):
    print(input_file_path)
    print(reference_file_path)
    print(output_file_path)
    
    
    # Ensemble pour stocker les valeurs du premier champ du premier fichier
    first_field_values = set()

    # Lire le premier fichier CSV et collecter les valeurs du premier champ
    with open(input_file_path, 'r', newline='') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            if row:  # Vérifier si la ligne n'est pas vide
                first_field_values.add(row[0])
                
    
    # Lire le deuxième fichier CSV, filtrer les lignes selon les valeurs du premier champ,
    # et écrire les lignes correspondantes dans le troisième fichier
    with open(reference_file_path, 'w+', newline='') as reference_file, open(output_file_path, 'w+', newline='') as output_file:
        reader = csv.reader(reference_file)
        writer = csv.writer(output_file)
        for row in reader:
            print(row[0])
            if row and row[0] in first_field_values:
                writer.writerow(row)
=======
    return json_data
>>>>>>> f4740638c725dbf2958098ade5037a177479bbfa
