from .relationsExtraction import *
from . import mes_variables 


def getRelations(selected_patterns, sentences_list_path, terms_list_path, relation_type, out_relation_path):
    
    mes_variables.SELECTED_PATTERNS_FROM_VIEWS=selected_patterns
    check_relations(get_sentences(sentences_list_path), get_terms(terms_list_path), relation_type, out_relation_path)




def getRelationsName():
    return get_relations_name("patterns.txt")

def getPatternsName(relations_name):
    return get_patterns_name("patterns.txt", relations_name)

def retreiveRelations(relationsFile_path):
    return get_relations(relationsFile_path)

def merge_relation_list(relations_files_list):
    merge_relations_list(relations_files_list)
    pathTo, FileName = os.path.split(relations_files_list[0])
    if os.path.isfile(str(pathTo) + '/liste_relation_fusionnée.csv'):
        return True
    else:
        return False

def reorganize_relations_list(relations_file):
    return reorganize_list_of_relations(relations_file)





def get_relations_name(list_patterns_path):
    fr_relations = open(list_patterns_path, "r")
    lines = fr_relations.readlines()
    relations_name = []
    for line in lines:
        if line[0] == "#" and line[1] != "#":
            relations_name.append(line.split('#')[1].strip())
    return relations_name

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

def get_patterns(list_patterns_path):
    fr_patterns = open(list_patterns_path, "r")
    lines = fr_patterns.readlines()
    patterns= []
    for line in lines:
        if line[0] != "#" and line != "" and line != "\n":
            patterns.append(line.strip().split('=')[0])
    fr_patterns.close()
    return patterns


def patterns_checkboxes(list_patterns_path):
    checkboxes=''
    fr_patterns = open(list_patterns_path, "r")
    lines = fr_patterns.readlines()
    for line in lines:
        
        if line[0] != "#" and line != "" and line != "\n":
            pattern=(line.strip().split('=')[0])
            
    fr_patterns.close()       
    return checkboxes

def get_relations_from_patterns(list_patterns):
    list_relations=[]
    for pattern in list_patterns :
        relation=get_relation_from_pattern(pattern)
        if not relation in list_relations :
            list_relations.append(relation)

    return list_relations

def get_relation_from_pattern(pattern):
    return pattern.split('_')[0]