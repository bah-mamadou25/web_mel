import zipfile
from django.http import HttpResponse, FileResponse
from django.views.generic import View
import os,time
from tika import parser
from pathlib import Path
import xml.etree.ElementTree as ET

def extract_file(zip_file_path):
    extract_to_path = 'data'  
    if zipfile.is_zipfile(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)  
        return True
    else:
        return False


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
                    return response
            except ValueError:
                time.sleep(1)