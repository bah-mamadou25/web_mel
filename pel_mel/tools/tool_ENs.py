import os,re,subprocess,shutil

import spacy
from .tool_load_file import read_text


def write_ENs(ENs_list, output_file_path):
    """

    :param ENs_list : liste des entités nommées
    :param output_file_path : chemin vers l'emplacement où on veut quavegarder le fichier
    """
    fw = open(output_file_path, 'w', encoding='UTF-8')
    for EN in ENs_list:
        fw.write(str(EN).strip())
        fw.write('\n')
    fw.close()

def read_ENs(input_file_path):
    """

    :param input_file_path: chemin vers le fichier
    :return : liste des éléments
    """
    my_list = []
    fr = open(input_file_path, 'r', encoding='UTF-8')
    lines = fr.readlines()
    for line in lines:
        my_list.append(str(line).strip())
    fr.close()
    return my_list

def get_number_of_sentences(corpus_path):
    """
    Renvoie le nombre de phrases d'un corpus donné
    :param corpus_path : chemin vers le corpus
    :return : nombre de phrases
    """
    
    fr = open(corpus_path, 'r', encoding='UTF-8')
    sentences = fr.readlines()
    return len(sentences)

def split_list_of_phrases(corpus_path):
    """
    Permet de diviser une longue liste de phrases sur plusieurs listes
    :param corpus_path : chemin vers le corpus
    """
    #pathTo, FileName = os.path.split(corpus_path)
    create_dir('data/bulky')

    os.system('split -l 12000 ' + corpus_path + ' data/bulky/')
    for file_name in os.listdir('data/bulky'):
        print(file_name)
        # Exécution de la fonction sur chaque nom de fichier
        get_named_entities('data/bulky/'+file_name, 'workspace/ENs/'+file_name+'_pers.csv', 'workspace/ENs/'+file_name+'_org.csv')

   


def get_named_entities(input_text_path, output_per_path, output_org_path):
    
    number_of_sentences = get_number_of_sentences(input_text_path)
    
    
    if number_of_sentences < 12050:
        ens_list = getENs(input_text_path)
        if len(ens_list[0]) > 1 and len(ens_list[1]) > 1:
            write_ENs(ens_list[0], output_per_path)
            write_ENs(ens_list[1], output_org_path)
            return True
        else:
            return False
    else:
        # le fichier est très volumineux, il faut le découper en plusieurs fichiers et renvoyer
        # un message d'erreur à l'interface
        split_list_of_phrases(input_text_path)

        return 'too_bulky'













def getENs(input_text_path):
    """

    :param input_text_path:
    :return:
    """
    ens_list = []
    per_list = []
    org_list = []
    corpus = read_text(input_text_path)
    nlp_fr = spacy.load("fr_core_news_md")
    nlp_fr.max_length = len(corpus) + 100
    doc = nlp_fr(corpus)
    for word in doc.ents:
        if word.label_ == "PER":
            if "." not in str(word).strip() and "0" not in str(word).strip() and "1" not in str(word).strip() and \
                    "2" not in str(word).strip() and "3" not in str(word).strip() and "4" not in str(word).strip() and \
                    "5" not in str(word).strip() and "6" not in str(word).strip() and "7" not in str(word).strip() and \
                    "8" not in str(word).strip() and "9" not in str(word).strip() and "©" not in str(word).strip() and \
                    "Ã" not in str(word).strip() and "madame" not in str(word).strip() and \
                    "Madame" not in str(word).strip() and "monsieur" not in str(word).strip() and \
                    "Monsieur" not in str(word).strip() and 1 < len(str(word).strip().split(' ')) < 3 and \
                    " -" not in str(word).strip() and "..." not in str(word).strip() and "…" not in str(word).strip() and \
                    "~" not in str(word).strip() and "!" not in str(word).strip() and "?" not in str(word).strip() and \
                    "à" not in str(word).strip() and "," not in str(word).strip() and ";" not in str(word).strip() and \
                    "s’" not in str(word).strip() and len(str(word)) > 2 and ":" not in str(word).strip() and \
                    str(word).strip()[len(str(word).strip())-1] not in ["-", ",", ".", "?", "!", "…", "'", "’", ":", "µ", "£"] and \
                    "(" not in str(word).strip() and ")" not in str(word).strip() and "/" not in str(word).strip() and \
                    "\\" not in str(word).strip():
                if str(word).strip() not in per_list:
                    per_list.append(str(word).strip())
        elif word.label_ == 'ORG':
            if "." not in str(word).strip() and "0" not in str(word).strip() and "1" not in str(word).strip() and \
                    "2" not in str(word).strip() and "3" not in str(word).strip() and "4" not in str(word).strip() and \
                    "5" not in str(word).strip() and "6" not in str(word).strip() and "7" not in str(word).strip() and \
                    "8" not in str(word).strip() and "9" not in str(word).strip() and "©" not in str(word).strip() and \
                    "Ã" not in str(word).strip() and len(str(word).strip()) > 2 and " -" not in str(word).strip() and \
                    "~" not in str(word).strip() and "!" not in str(word).strip() and "?" not in str(word).strip() and \
                    "à" not in str(word).strip() and "," not in str(word).strip() and ";" not in str(word).strip() and \
                    "s’" not in str(word).strip() and "…" not in str(word).strip() and \
                    str(word).strip()[len(str(word).strip())-1] not in ["-", ",", ".", "?", "!", "…", "'", "’", ":", "µ", "£"] and \
                    "(" not in str(word).strip() and ")" not in str(word).strip() and "/" not in str(word).strip() and \
                    "\\" not in str(word).strip():
                if str(word).strip() not in org_list:
                    org_list.append(str(word).strip())
    ens_list.append(sorted(per_list))
    ens_list.append(sorted(org_list))
    return ens_list

def get_named_entities(input_text_path, output_per_path, output_org_path):
    number_of_sentences = get_number_of_sentences(input_text_path)
    if number_of_sentences < 12050:
        ens_list = getENs(input_text_path)
        if len(ens_list[0]) > 1 and len(ens_list[1]) > 1:
            write_ENs(ens_list[0], output_per_path)
            write_ENs(ens_list[1], output_org_path)
            return True
        else:
            return False
    else:
        # le fichier est très volumineux, il faut le découper en plusieurs fichiers et renvoyer
        # un message d'erreur à l'interface
        split_list_of_phrases(input_text_path)
        return 'too_bulky'
    

def create_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
