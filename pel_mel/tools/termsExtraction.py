# -*- coding: utf-8 -*-

import os
import re
import subprocess

import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from .tool_ENs import create_dir


stemmer = SnowballStemmer(language='french')
nlp = spacy.load('fr_core_news_md')
nlp.max_length = 2000000 
def get_lemma(sentence):
    doc = nlp(sentence)
    return [token.lemma_ for token in doc]

"""
lecture d'un fichier de termes avec 3 colonnes : terme | score | source
renvoie liste d'objets Term(terme, score, source)
"""
def file_to_list(terms_file_path):
    fr = open(terms_file_path, "r", encoding="UTF-8")
    lines = fr.readlines()
    myList = []
    for line in lines:
        m_term = Term(str(line).split(';')[0], str(line).split(';')[1], str(line).split(';')[2])
        myList.append(m_term)
    return myList


def get_number_of_sentences(corpus_path):
    """
    Renvoie le nombre de phrases d'un corpus donné
    :param corpus_path : chemin vers le corpus
    :return : nombre de phrases
    """
    fr = open(corpus_path, 'r', encoding='UTF-8')
    sentences = fr.readlines()
    return len(sentences)




def merge_files(terms_files_list):
    """
    Permet de fusionner plusieurs listes de termes avec un petit nettoyage
    :param terms_files_list : chemins vers les fichiers sélectionnés
    """
    terms_list = []
    for file in terms_files_list:
        fr = open(str(file), 'r', encoding='UTF-8')
        terms = fr.readlines()
        for term in terms:
            if term not in terms_list:
                m_term = Term(str(term).split(';')[0], str(term).split(';')[1], str(term).split(';')[2])
                terms_list.append(m_term)
        fr.close()
    if len(terms_list) > 0:
        cleaned_list = cleanUpTerms(terms_list)
        pathTo, FileName = os.path.split(terms_files_list[0])
        fw = open(str(pathTo) + '/liste_termes_fusionnée.csv', 'w', encoding='UTF-8')
        for term in cleaned_list:
            fw.write(str(term.term).strip() + ";" + str(term.score).strip() + ";" + str(term.source).strip())
            fw.write('\n')
        fw.close()


"""
création de fichier de configuration d'entrée à l'extracteur de termes
exécution de l'extracteur
renvoie True si l'extracteur a donné un fichier contenant les termes en sortie
False sinon
"""
def termsExtraction(corpus_path, termsExtracted_path, STEM, METODE_SCORING, LONGUEURMIN, LONGUEURMAX):
    print("Création de fichier de configuartion d'entrée à l'extrateur de termes...")
    fichier_config = open("config/fichier_config.cfg", "w")
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

    process = subprocess.Popen(["python", "workspace/termes/extractionTerme.py", "config/fichier_config.cfg"])
    process.wait()
    print("Fin d'exécution de l'extracteur de termes !")
    if os.path.exists(termsExtracted_path):
        return True
    else:
        return False

"""
lecture d'un fichier contenant les termes
prendre à partir de la 2ème ligne
ne prendre que les colonnes 2 et 3
renvoie une liste d'objets Term(term, score, source)
"""
def retreiveTerms(list_terms_path):
    print("Récupération de la liste des termes à traiter...")
    fr = open(list_terms_path, "r", encoding="UTF-8")
    lines = fr.readlines()
    terms_list = []
    line_index = 1
    for line in lines:
        if line_index > 1:
            m_term = Term(str(line).split(';')[1], str(line).split(';')[2], "_")
            terms_list.append(m_term)
        line_index = line_index + 1
    fr.close()

    return terms_list


class Term:
    def __init__(self, term, score, source):
        self.term = term
        self.score = score
        self.source = source

    def setTerm(self, new_term):
        self.term = new_term

    def getSource(self):
        return self.source

    def setSource(self, src):
        self.source = self.source + "," + str(src)



"""
nettoyage de la liste des termes
supprimer les termes < 2 caractères
supprimer les stop-words
termes contanant (que, qui, qu', et, nombre)
"""
def cleanUpTerms(terms_list):
    print("Premier nettoyage de la liste des termes à traiter...")
    terms_list_cleaned = []
    stop_words = set(stopwords.words('french'))
    for term in terms_list:
        if len(str(term.term).strip()) > 3:
            if " que " not in str(term.term) and " qui " not in str(term.term) and " qu'" not in str(term.term) and " et " not in str(term.term) and bool(re.search(r'\d', str(term.term).strip())) == False:
                if str(term.term).strip()[len(str(term.term).strip()) - 1] == "’":
                    term.setTerm(str(term.term)[:-3])
                if "«" in str(term.term):
                    term.setTerm(str(term.term).replace("«", ""))
                if "»" in str(term.term):
                    term.setTerm(str(term.term).replace("»", ""))
                if "%" in str(term.term):
                    term.setTerm(str(term.term).replace("%", ""))
                if "$" in str(term.term):
                    term.setTerm(str(term.term).replace("$", ""))
                if "€" in str(term.term):
                    term.setTerm(str(term.term).replace("€", ""))
                if "_" in str(term.term):
                    term.setTerm(str(term.term).replace("_", ""))
                if " - " in str(term.term):
                    term.setTerm(str(term.term).replace(" - ", " "))
                if "/" in str(term.term):
                    term.setTerm(str(term.term).replace("/", ""))
                if "' " in str(term.term):
                    term.setTerm(str(term.term).replace("' ", "'"))
                if "’ " in str(term.term):
                    term.setTerm(str(term.term).replace("’ ", "'"))
                word_tokens = word_tokenize(str(term.term).strip())
                if len(word_tokens) > 1:
                    terms_list_cleaned.append(term)
                elif len(word_tokens) == 1:
                    if word_tokens[0] not in stop_words:
                        terms_list_cleaned.append(term)
    return terms_list_cleaned


"""
création de la liste des termes de référence à partir de plusieurs fichiers
"""
def createListTermsReference(termsReferencePaths):
    print("Création de la liste des termes de référence...")
    thesaurus_terms_list = []
    for termsReferencePath in termsReferencePaths:
        fr = open(str(termsReferencePath), "r", encoding="UTF-8")
        termsReference = fr.readlines()
        for termReference in termsReference:
            trouv = False
            for z in range(len(thesaurus_terms_list)):
                if str(termReference).strip() == str(thesaurus_terms_list[z].term).strip():
                    thesaurus_terms_list[z].setSource(str(os.path.splitext(os.path.basename(termsReferencePath))[0]))
                    # print("le term existe deja : " + str(thesaurus_terms_list[z].term).strip() + "\t" + str(thesaurus_terms_list[z].source).strip())
                    trouv = True
                    break
            if trouv == False:
                m_term = Term(str(termReference).split(';')[0], str("0"), str(os.path.splitext(os.path.basename(termsReferencePath))[0]))
                thesaurus_terms_list.append(m_term)
        fr.close()
    return thesaurus_terms_list

"""
validation automatique des termes : intersection termes & termes de référence
en entrée :
chemin vers la liste des termes à traiter
chemin vers la liste des listes des termes utilisés comme références
en sortie :  liste des termes valides
"""
def automaticTermValidation(terms_list, termsReferencePaths):
    print("Validation automatique des termes.")
    # Récupération de la liste des termes de références
    thesaurus_terms_list = createListTermsReference(termsReferencePaths)
    valid_terms_list = []
    for term in terms_list:
        first_carac = str(term).split(';')[0].strip()[0]
        longueur = len(word_tokenize(str(term).split(';')[0].strip()))
        for thesaurus_term in thesaurus_terms_list:
            if str(thesaurus_term.term).strip()[0].lower() == first_carac.lower():
                if len(word_tokenize(str(thesaurus_term.term).strip())) == longueur:
                    if get_lemma(str(term).split(';')[0].strip()) == get_lemma(str(thesaurus_term.term).strip()):
                        valid_terms_list.append(str(term).split(';')[0].strip() + ";" + str(term).split(';')[1].strip() + ";" + str(thesaurus_term.source).strip())
                        break
    return valid_terms_list


def getTermsSources(terms_file_path):
    fr = open(str(terms_file_path), "r", encoding="UTF-8")
    sources_list = []
    sources_list.append("Tous")
    lines = fr.readlines()
    for line in lines:
        sources = (line.strip().split(";")[2]).strip().split(",")
        for x in range(len(sources)):
            if sources[x] not in sources_list:
                sources_list.append(sources[x])
    fr.close()
    return sources_list