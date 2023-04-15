import os
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
    create_dir('data/bulky')

    os.system('split -l 12000 ' + corpus_path + ' data/bulky/')
    for file_name in os.listdir('data/bulky'):
        print(file_name)
        # Exécution de la fonction sur chaque nom de fichier
        terms_extraction('data/bulky/'+file_name, 'workspace/termes/'+file_name+'_termes.csv', STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX)