# -*- coding: utf-8 -*-
import os,ast

import spacy
from spacy.matcher import Matcher

from .termsExtraction import Term
from . import mes_variables 

# Renvoie une liste contenant les noms des relations existantes
# en entrée : chemin vers le fichier contenant les relations
# en sortie : liste des noms des relations
def get_relations_name(list_patterns_path):
    fr_relations = open(list_patterns_path, "r")
    lines = fr_relations.readlines()
    relations_name = []
    for line in lines:
        if line[0] == "#" and line[1] != "#":
            relations_name.append(line.split('#')[1].strip())
    return relations_name


# Renvoie une liste contenant les noms des patrons d'un type de relation donné
# en entrée : chemin vers le fichier contenant les patrons et le type de relation recherchée
# en sortie : liste des noms des patrons
def get_patterns_name(list_patterns_path, relations_name):
    fr_patterns = open(list_patterns_path, "r")
    lines = fr_patterns.readlines()
    patterns_name = []
    for line in lines:
        if line[0] != "#" and line != "" and line != "\n":
            for relation_name in relations_name:
                if str(relation_name).strip() == (line.strip().split('=')[0]).split('_')[0]:
                    patterns_name.append(line.strip().split('=')[0])
    fr_patterns.close()
    return patterns_name


# renvoie la liste des phrases à partir du fichier txt contenant les phrases
def get_sentences (sentencesFile_path):
    print("Récupération des phrases...")
    sentences_list = []
    fr_sentences = open(sentencesFile_path, "r")
    lines = fr_sentences.readlines()
    for line in lines:
        sentences_list.append(line.strip())
    fr_sentences.close()
    return sentences_list


# renvoie la liste des objets Term à partir du fichier
def get_terms(list_terms_path):
    print("Récupération des termes...")
    fr = open(list_terms_path, "r", encoding="UTF-8")
    lines = fr.readlines()
    terms_list = []
    for line in lines:
        m_term = Term(str(line).split(';')[0], str(line).split(';')[1], str(line).split(';')[2])
        terms_list.append(m_term)
    fr.close()
    return terms_list


# vérifie si une phrase contient les 2 termes dans l'ordre : term_1 patron term_2
def get_candidate_sentences(sentence, terms_list, relation, relation_type, out_relation):
    for term1 in range(0, len(terms_list)-1):
        for term2 in range(term1+1, len(terms_list)):
            if str(terms_list[term1].term).strip() != str(terms_list[term2].term).strip():
                if " "+str(terms_list[term1].term).strip()+" " in sentence and " "+str(terms_list[term2].term).strip()+" " in sentence:
                    if (" " + str(terms_list[term1].term).strip() + " " not in relation) and (" " + str(terms_list[term2].term).strip() + " " not in relation):
                        if (sentence.find(" " + str(terms_list[term1].term).strip() + " ") < sentence.find(relation) < sentence.find(" " + str(terms_list[term2].term).strip() + " ")):
                            out_relation.write(str(terms_list[term1].term).strip()+";"+str(terms_list[term2].term).strip()+";"+relation+";"+relation_type+";"+sentence)
                            out_relation.write("\n")
                            # m_relation = Relation(str(terms_list[term1].term).strip(), str(terms_list[term2].term).strip(), relation, relation_type, sentence)
                            # relations_list.append(m_relation)
                        elif (sentence.find(" " + str(terms_list[term2].term).strip() + " ") < sentence.find(relation) < sentence.find(" " + str(terms_list[term1].term).strip() + " ")):
                            out_relation.write(str(terms_list[term2].term).strip()+";"+str(terms_list[term1].term).strip()+";"+relation+";"+relation_type+";"+sentence)
                            out_relation.write("\n")
                            # m_relation = Relation(str(terms_list[term2].term).strip(), str(terms_list[term1].term).strip(), relation, relation_type, sentence)
                            # relations_list.append(m_relation)


# vérifie si une phrase respecte un patron
def check_relations(sentences_list, terms_list, relation_type, out_relation_path):
    out_relation = open(out_relation_path, "w", encoding="UTF-8")
    # relations_list = []
    nlp = spacy.load('fr_core_news_md')
    matcher = Matcher(nlp.vocab)
    matcher.add("relation", getRelations()) # relations provient de 'tool_relationsPatterns.py'
    for sentence in sentences_list:
        doc = nlp(sentence)
        if len(doc) > 20:
            sents = sentence.split(',')
            matches = matcher(doc)
            for match_id, start, end in matches:
                if len(doc[start:end]) > 0:
                    for sent in sents:
                        get_candidate_sentences(sent, terms_list, str(doc[start:end]), relation_type, out_relation)
        else:
            matches = matcher(doc)
            for match_id, start, end in matches:
                if len(doc[start:end]) > 0:
                        get_candidate_sentences(sentence, terms_list, str(doc[start:end]), relation_type, out_relation)
    out_relation.close()
    # return relations_list


# Récupère les relations à partir d'un fichier passé en paramètres
# Renvoie les relations sous forme d'une liste
def get_relations(relationsFile_path):
    print("Récuparation des relations...")
    relations_list = []
    fr_relations = open(relationsFile_path, "r")
    lines = fr_relations.readlines()
    for line in lines:
        m_relation = Relation(str(line).split(';')[0], str(line).split(';')[1], str(line).split(';')[2], str(line).split(';')[3], str(line).split(';')[4])
        relations_list.append(m_relation)
    fr_relations.close()
    return relations_list


def cleanUpRelations(relations_list):
    print("Nettoyage de la liste des relations...")
    cleaned_relations_list = []
    if len(relations_list) > 0:
        cleaned_relations_list.append(relations_list[0])
        for relation in relations_list:
            trouv = False
            for cleaned_relation in cleaned_relations_list:
                if str(relation.term1).strip() == str(cleaned_relation.term1).strip() and str(relation.term2).strip() == str(cleaned_relation.term2).strip() and str(relation.patern).strip() == str(cleaned_relation.patern).strip():
                    trouv = True
                    break
            if trouv == False:
                cleaned_relations_list.append(relation)
    return cleaned_relations_list


def merge_relations_list(relations_files_list):
    """
    Fusionner plusieurs listes de relations
    :param relations_files_list:
    """
    relations_list = []
    for file in relations_files_list:
        fr = open(str(file), 'r', encoding='UTF-8')
        relations = fr.readlines()
        for relation in relations:
            if relation not in relations_list:
                m_relation = Relation(str(relation).split(';')[0], str(relation).split(';')[1], str(relation).split(';')[2], str(relation).split(';')[3], str(relation).split(';')[4])
                relations_list.append(m_relation)
        fr.close()
    if len(relations_list) > 0:
        pathTo, FileName = os.path.split(relations_files_list[0])
        fw = open(str(pathTo) + '/liste_relation_fusionnée.csv', 'w', encoding='UTF-8')
        for rel in relations_list:
            fw.write(str(rel.term1).strip()+";"+str(rel.term2).strip()+";"+str(rel.patern).strip()+";"+str(rel.relation).strip()+";"+str(rel.sentence).strip())
            fw.write('\n')
        fw.close()


def reorganize_list_of_relations(relations_file):
    reorganized_list = []
    fr = open(str(relations_file), 'r', encoding='UTF-8')
    relations = fr.readlines()
    for rel in relations:
        m_relation = ""
        T1 = rel.split(';')[0]
        m_relation = T1
        for re in relations:
            if T1 == re.split(';')[0]:
                m_relation = m_relation + ';' + re.split(';')[1]
        if m_relation not in reorganized_list:
            reorganized_list.append(m_relation)
    return reorganized_list

# Classe Relation(term_1, term_2, patron, relation, phrase)
class Relation:
    def __init__(self, term1, term2, patern, relation, sentence):
        self.term1 = term1
        self.term2 = term2
        self.patern = patern
        self.relation = relation
        self.sentence = sentence

def getRelations():
    fr = open("patterns.txt", "r")
    lines = fr.readlines()
    relations=[]
    for selected_pattern in mes_variables.SELECTED_PATTERNS_FROM_VIEWS:
        for line in lines:
            if line[0] != "#":
                if str(selected_pattern).strip() == str(line.split('=')[0].strip()):                                 
                    relations.append(ast.literal_eval(line.split('=')[1].strip().split('],')[0]+']'))        
    return relations