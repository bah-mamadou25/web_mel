import zipfile
from django.http import HttpResponse, FileResponse
from django.views.generic import View
import os,time,shutil,re
import nltk
from tika import parser
from pathlib import Path
import xml.etree.ElementTree as ET

def extract_file(zip_file_path):
    extract_to_path = os.path.dirname(zip_file_path) 

    
    if zipfile.is_zipfile(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            print('Extracting files to: ', extract_to_path)
            # zip_ref.printdir()  # Afficher la liste des fichiers dans le fichier zip
            zip_ref.extractall(extract_to_path)  
        return True
    else:
        return False


def delete_content(directory):
    if os.path.exists(directory):
    # Bouclez sur tous les fichiers et sous-répertoires dans le répertoire
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            # Supprimez le fichier ou le sous-répertoire
            try:
                if os.path.isfile(filepath):
                    os.unlink(filepath)
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath, ignore_errors=True)
            except Exception as e:
                print(f"Erreur lors de la suppression de {filepath} : {e}")
    else:
        print(f"Le répertoire {directory} n'existe pas.")

def createCorpus(input_path, output_path):
    """
    Création d'un corpus texte à partir de plusieurs répertoires/sous-répertoires
    contenant des fichiers .doc, .docx .txt ou .pdf
    :param input_path: le chemin complet vers le répertoire père contenant les sous-répertoire/fichiers à traiter
    :param output_path: le chemin complet où vous voulez stocker le fichier de sortie
    """
    
    files_processed = 0
    output_file = open(output_path, "w")
    for rootdir, dirs, files in os.walk(input_path):
        for file in files:
            print(file)
            if file.endswith(('.pdf', '.doc', '.docx', '.DOC', '.DOCX', '.txt')):
                filename = os.path.join(rootdir, file)
                file_parsed = parser.from_file(filename)
                output_file.write(str(file_parsed['content']))
                files_processed = files_processed + 1

            if file.endswith('.xml') or file.endswith('.XML'):
                filename = os.path.join(rootdir, file)
                tree = ET.parse(filename)
                root = tree.getroot()
                if root.findall('TextContent'):
                    text_by_file = ""
                    for TextContent in root.findall('TextContent'):
                        text_by_file += TextContent.text + " "
                    output_file.write(str(text_by_file))
                    files_processed = files_processed + 1
    output_file.close()
    print("Corpus créé: " + output_path.strip())
    print("Nombre total de fichiers traités ", files_processed)

def download_corpus(path):
        filepath = os.path.join(os.getcwd(), path)
        
        # Vérifier si le fichier est fermé
        while True:
            try:
                with open(filepath, "rb") as f:
                    # Lire le contenu du fichier
                    fichier_bytes = f.read()
                    # Renvoyer le fichier en tant que réponse HTTP pour téléchargement direct
                    response = HttpResponse(fichier_bytes, content_type="application/force-download")
                    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(filepath)
                    if response :
                        delete_content('data')
                        delete_content('workspace')
                    return response
            except ValueError:
                time.sleep(1)

def download_directory_as_zip(path):
    """
    Télécharger tous les fichiers dans un répertoire donné sous forme de fichier zip.
    """
    # Chemin absolu du répertoire
    dirpath = os.path.join(os.getcwd(), path)
    
    # Créer un nom de fichier unique pour le fichier zip
    zip_filename = os.path.basename(dirpath) + '.zip'
    
    # Créer un objet ZipFile et ajouter chaque fichier du répertoire au fichier zip
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, dirpath))
    
    # Ouvrir le fichier zip en mode lecture binaire
    with open(zip_filename, 'rb') as f:
        # Lire le contenu du fichier zip
        zip_bytes = f.read()
        
        # Renvoyer le fichier en tant que réponse HTTP pour téléchargement direct
        response = HttpResponse(zip_bytes, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % zip_filename
        

        # Supprimer le fichier zip après l'avoir envoyé en tant que réponse HTTP
        os.remove(zip_filename)

        if response :
            delete_content('data')
            delete_content('workspace')
        
        return response
    

def deleteURL(line):
    """
    Identifie les URL dans une chaîne de caractères et les remplace par ""
    :param line:
    :return: ligne nettoyée
    """
    regex_url = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url_list = re.findall(regex_url, line)
    for url in url_list:
        line = line.replace(url[0], "")
    return line

def repl_func(match):
  if match == True:
    return ""


def cleanUpCorpus(old_corpus_path, new_corpus_path):
    """
    Nettoyage d'un corpus :
    suppression des lignes qui ont moins de 5 caractères
    suppression des lignes qui n'ont pas de lettres (i.e. que des chiffres, caractères spéciaux...)
    :param old_corpus_path : le chemin vers le corpus à traiter
    :param new_corpus_path : le chemin où vous voulez stocker le corpus traité
    """
    print("Nettoyage du corpus: " + old_corpus_path.strip())
    old_corpus = open(old_corpus_path, "r")
    new_corpus_list = []

    regex = re.compile('[a-zA-Z]')
    lines = old_corpus.readlines()
    for line in lines:
        if len(line) > 10:
            if regex.search(line) != None:
                n_line = deleteURL(line)
                new_corpus_list.append(n_line)
    old_corpus.close()

    # création du corpus nettoyé (avec retour à la ligne)
    new_corpus = open(old_corpus_path, "w")
    for line in new_corpus_list:
        new_corpus.write(line)
    new_corpus.close()

    # suppression des retours à la ligne
    print("Suppression des retours inutiles à la ligne... remplacement...")
    corpus = Path(old_corpus_path).read_text()\
        .replace("«", "") \
        .replace("»", "") \
        .replace("{", "") \
        .replace("}", "") \
        .replace("*", "") \
        .replace("/", "") \
        .replace("--", "") \
        .replace("  ", "") \
        .replace("_", "") \
        .replace("...", ".") \
        .replace(" .", ".") \
        .replace(" ,", ",") \
        .replace("C’ ", "C'") \
        .replace("C ’", "C'") \
        .replace("S’ ", "S'") \
        .replace("S ’", "S'") \
        .replace("D’ ", "D'") \
        .replace("D ’", "D'") \
        .replace("L’ ", "L'") \
        .replace("L ’", "L'") \
        .replace("c’ ", "c'") \
        .replace("c ’", "c'") \
        .replace("s’ ", "s'") \
        .replace("s ’", "s'") \
        .replace("d’ ", "d'") \
        .replace("d ’", "d'") \
        .replace("l’ ", "l'") \
        .replace("l ’", "l'") \
        .replace("C' ", "C'") \
        .replace("C '", "C'") \
        .replace("S' ", "S'") \
        .replace("S '", "S'") \
        .replace("D' ", "D'") \
        .replace("D '", "D'") \
        .replace("L' ", "L'") \
        .replace("L '", "L'") \
        .replace("c' ", "c'") \
        .replace("c '", "c'") \
        .replace("s' ", "s'") \
        .replace("s '", "s'") \
        .replace("d' ", "d'") \
        .replace("d '", "d'") \
        .replace("l' ", "l'") \
        .replace("l '", "l'") \
        .replace('.- ', '. ') \
        .replace('-\n', '') \
        .replace('\n', ' ') \
        .replace('\t', '') \
        .replace('( ', '(') \
        .replace(' )', ')') \
        .replace("' ", "'") \
        .replace("’ ", "'") \
        .replace(';', ',') \
        .replace('<', '') \
        .replace("\\s+", " ") \
        .replace('>', '')\
        .replace('/', ' ') \
        .replace('@', ' ') \
        .replace('+', '') \
        .strip()
    new_corpus = open(new_corpus_path, "w")
    new_corpus.write(corpus.strip())
    new_corpus.close()
    print("Corpus nettoyé: ", new_corpus_path.strip())

def read_text(input_text_path):
    """
    Permet de lire un fichier texte
    :param input_text_path: le chemin complet vers le fichier à lire
    :return : le contenu lu sous forme de chaine de caractères
    """
    print("Lecture de : " + input_text_path.strip())
    input_text = Path(input_text_path).read_text()
    return input_text


def readText(input_text_path):
    text = read_text(input_text_path)
    return str(text)

def getSentences(input_text):
    """
    Tokenisation par phrases & petit nettoyage
    :param input_text: le chemin complet vers le fichier texte à traiter
    :return: liste des phrases
    """
    print("Extraction des phrases...")
    sentences = nltk.sent_tokenize(input_text, language='french')
    regex = re.compile('[a-zA-Z]')
    for sentence in sentences:
        if len(sentence) < 5 or regex.search(sentence) == None:
            sentences.remove(sentence)
    return sentences


def retrieveSentences(input_text_path):
    input_text = read_text(input_text_path)
    sentences = getSentences(input_text)
    # préparation du répertoire de destination
    pathTo, FileName = os.path.split(input_text_path)
    FileName = Path(input_text_path).stem
    sentences_extracted_path = pathTo + "/" + "sentences_"+FileName+".txt"
    # Ecriture des phrases
    print("Création du fichier de sortie contenant les phrases")
    output_sentences = open(sentences_extracted_path, "w")
    cpt = 1
    for sentence in sentences:
        output_sentences.write(str(sentence).replace("\n", " ").replace("\t", ""))
        output_sentences.write("\n")
        cpt = cpt + 1
    output_sentences.close()
    print("Nombre total de phrases :", cpt)
    return str(sentences_extracted_path)