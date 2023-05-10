# -*- coding: utf-8 -*-

import os
import random
import re,csv

import gensim
from tika import parser
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from .tool_load_file import *
from django.utils.html import escape
from django.urls import reverse

def prepare_themes_for_doc2vec(corpus_path,themes_by_level_list, messages_directory_path):
    prepare_thematique_for_doc2vec(corpus_path,themes_by_level_list, messages_directory_path)

def msg_presse_classification(folder_path, thematique_path, thematiques_1_level_path, thematiques_2_level_path,
                                   thematiques_3_level_path, vector_size, min_count, epochs, output_result_path):
    messages_presse_classification(folder_path, thematique_path, thematiques_1_level_path, thematiques_2_level_path,
                                   thematiques_3_level_path, vector_size, min_count, epochs, output_result_path)
    if os.path.exists(output_result_path):
        return True
    else:
        return False


def retreive_classified_messages(file_path):
    return retreive_classified_msg(file_path)







def prepare_thematique_for_doc2vec(corpus_path,themes_by_level_list, messages_directory_path):
    if not os.path.exists(messages_directory_path):
        os.makedirs(messages_directory_path)

    corpus = read_text(corpus_path)

    with open(themes_by_level_list, 'r', encoding='UTF-8') as fr:
        my_file = fr.readlines()
        for line in my_file:
            if len(line) >= 1:
                terms = (line.split(';')[1]).split(', ')
                print('------------------------')
                print(terms)
                print('------------------------')

                with open(messages_directory_path + '/' + line.split(';')[0] + '.csv', 'w', encoding='UTF-8') as fw:
                    fw.write('Valide\tTerme\tFrequence\tProposition\n')
                    for term in terms:
                        if " " + term + " " in corpus:
                            fw.write("v\t" + term.replace(" ", "_") + '\t' + str(random.randint(0, 150)) + '\t' + 'x')
                            fw.write('\n')

                    fw.close()
def read_thematique(thematiques_path):
    fr_thematiques = open(thematiques_path, 'r', encoding='UTF-8')
    thematiques = fr_thematiques.readlines()
    thematique_list = []
    for them in thematiques:
        thematique_list.append(str(them).strip())
    return thematique_list


#Afin de les utiliser dans views.py pour generer les fichiers
folder = []
text = []
def messages_presse_classification(folder_path, thematique_path, thematiques_1_level_path, thematiques_2_level_path,
                                   thematiques_3_level_path, vector_size, min_count, epochs, output_result_path):
    # lire les thématiques
    thematique_1_list = read_thematique(thematiques_1_level_path)
    thematique_2_list = read_thematique(thematiques_2_level_path)
    thematique_3_list = read_thematique(thematiques_3_level_path)

    # mettre toutes les thématiques dans une liste
    thematique_list = []
    thematique_list.append(thematique_1_list)
    thematique_list.append(thematique_2_list)
    thematique_list.append(thematique_3_list)

    message = []
    originatingId = []
    title = []
    

    # Récupérer le contenu textuel (balise TextContent)
    for rootdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xml') or file.endswith('.XML'):
                filename = os.path.join(rootdir, file)
                tree = ET.parse(filename)
                root = tree.getroot()

                if root.findall('TextContent'):
                    text_by_file = ""
                    title_by_file = ""
                    folder.append(rootdir)
                    for TextContent in root.findall('TextContent'):
                        text_by_file += TextContent.text + " "
                    text.append(text_by_file)

                    for Title in root.findall('Title'):
                        title_by_file += Title.text + " "
                    title.append(title_by_file)

                    for Oid in root.findall('OriginatingSystemId'):
                        originatingId.append(re.sub('<>', '', Oid.text))
                    message.append([rootdir, re.sub('<>', '', root.find('OriginatingSystemId').text), title_by_file, text_by_file, root.find("SentDate").text])
                    
                    for t in text :
                        print(t)
                        print("\n******************\n")
                    
                    print(len(text))
                    print(len(folder))

    # Créer le data frame
    message_pd = pd.DataFrame(message, columns=["Dossier", "Id", "Titre", "Corps", "DateEnvoi"])
    message_pd["Text_simple"] = [re.compile("\n.*De.*:").split(s)[0] for s in message_pd["Corps"]]

    # pièces jointes
    Mail_PJ_titre = []
    poubelle = ['Tous droits de reproduction réservés']

    for i, p in message_pd.iterrows():
        final = p["Titre"] + "\n" + p["Text_simple"]

        for r, d, files in os.walk(p["Dossier"]):
            for file in files:
                if (file.endswith(('.pdf', '.doc', '.docx', '.DOC', '.DOCX', '.txt', '.TXT'))):
                    filename = os.path.join(r, file)
                    file_parsed = parser.from_file(filename)
                    text_by_file = file_parsed['content']
                    text_by_file = str(text_by_file).replace('.- ', '. ').replace('-\n', '').replace('\t', '')\
                        .replace('( ', '(').replace(' )', ')').replace("' ", "'").replace("_", " ").strip()
                    text_by_file = re.sub("[^a-zA-ZÀ-ÿ\n\-\’. ]*", "", text_by_file)
                    text_by_file = re.sub('  +', " ", text_by_file)
                    for p in poubelle:
                        text_by_file = text_by_file.replace(p, "").strip()
                    final += file.split(".")[0] + '\n'
                    for l in text_by_file.split('\n'):
                        if len(l.split()) > 3:
                            final += l+'\n'

        Mail_PJ_titre.append(final)

    message_pd["Mail_PJ_titre"] = Mail_PJ_titre

    # Entraîner le modèle Doc2Vec
    doc = []
    for i, line in enumerate(message_pd["Mail_PJ_titre"].values):
        tokens = gensim.utils.simple_preprocess(line)
        doc.append(gensim.models.doc2vec.TaggedDocument(tokens, [i]))
    d2v = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=min_count, epochs=epochs)
    d2v.build_vocab(doc)
    d2v.train(doc, total_examples=d2v.corpus_count, epochs=d2v.epochs)

    pd_thematique = pd.DataFrame()

    for filename in os.listdir(thematique_path):
        f = os.path.join(thematique_path, filename)
        if os.path.isfile(f):
            them = f.split("/")[-1].replace(".csv", "")
            if len(pd.read_csv(f, sep="\t")["Terme"]) > 0:
                pd_thematique[them] = pd.read_csv(f, sep="\t")["Terme"]
    # pd_thematique.to_csv(folder_path + "thematique_x.csv", sep=';', index=None)

    for niveau, ths in enumerate(thematique_list):
        ranks = []
        col = []
        for th in ths:
            if th in pd_thematique.columns:
                # inferred_vector_th = d2v.infer_vector([th] + pd_thematique[th])??:: modif
                
                inferred_vector_th = d2v.infer_vector([str(x) for x in [th] + pd_thematique[th].values.tolist()])

                
                sims = d2v.docvecs.most_similar([inferred_vector_th], topn=len(d2v.docvecs))
                rank = pd.DataFrame([[a, b] for a, b in sims]).sort_values(0)[1].values
                ranks.append(rank)
                col.append(th)

                
    

        if len(ranks) > 0:
            df_res_them = pd.DataFrame(np.transpose(ranks), columns=col)
            message_pd["labels_niveau"+str(niveau+1)] = df_res_them.idxmax(axis=1)

    df_final_columns = ["Id", "labels_niveau1"]
    if "labels_niveau2" in message_pd.columns:
        df_final_columns.append("labels_niveau2")
    if "labels_niveau3" in message_pd.columns:
        df_final_columns.append("labels_niveau3")
    
    df_final = message_pd[df_final_columns]
    df_final.to_csv(output_result_path, sep=';', index=None, encoding='UTF-8')

def retreive_classified_msg(file_path):
    fr = open(file_path, 'r', encoding='UTF-8')
    my_file = fr.readlines()
    classified_msg = []
    if len(my_file) > 0 :
        cpt = 0
        for line in my_file:
            if cpt > 0:
                classified_msg.append(line)
            cpt = cpt + 1
        return classified_msg
    else:
        return "no_result"
    
    
def csv_no_header_to_html_table(csv_path):
    """
    Convertit un fichier CSV en une table HTML.

    :param csv_path: Le chemin d'accès du fichier CSV à convertir.
    :type csv_path: str
    :return: Une chaîne de caractères représentant une table HTML avec les données du fichier CSV.
    :rtype: str
    """
    html_table = ""
    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader) # Ignore la première ligne
        for i, row in enumerate(reader):
            html_table += "<tr>"
            for data in row:
                html_table += "<td>'{}'</td>".format(escape(data))
            if len(row) == 3:
                html_table += "<td></td>" # revoir pourquoi bug pour niveau 3
<<<<<<< HEAD
            url = reverse('voirdoc') + '?id=' + str(i+16)
=======
            url = reverse('voirdoc') + '?id=' + str(i+1)
>>>>>>> f4740638c725dbf2958098ade5037a177479bbfa
            html_table += '<td><a href="{}">voir</a></td>'.format(url)
            html_table += "</tr>\n"

    return html_table




def create_files_from_source(lst_txt, lst_folder, directory_path):
    """
    Crée des fichiers texte à partir d'une liste de texte, en ajoutant une ligne de répertoire au début de chaque fichier.

    Args:
        lst_txt (list): Liste de texte à écrire dans les fichiers.
        lst_folder (list): Liste de noms de répertoires correspondant à chaque élément de texte.
        directory_path (str): Chemin d'accès au répertoire dans lequel les fichiers doivent être créés.

    Returns:
        None
    """
    for index, element in enumerate(lst_txt, start=0):
        file_path = os.path.join(directory_path, f'{index+1}.txt')
        content = "## REPERTOIRE : {} ## \n{}".format(lst_folder[index].split('data/')[1], element)
        with open(file_path, 'w') as file:
            file.write(content)

        print(f'Le fichier {file_path} a été créé avec succès.')
