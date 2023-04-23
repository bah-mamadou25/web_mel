    # -*- coding: utf-8 -*-

import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec, KeyedVectors




def preprocessing_word2vec(corpus_path, lowercase, del_ponctuation, lemm, del_stopwords, rmv_words_less_than_3_chars):
    """
    Cette fonction fait appel au model word2vec dans le package tools
    :param corpus_path : chemin vers le corpus qu'on veut traiter
    :param lowercase : rendre la totalité du texte en minuscule
    :param del_ponctuation : supprimer les ponctuations
    :param lemm : lemmatisation
    :param del_stopwords : supprimer les mots vides
    :param rmv_words_less_than_3_chars : supprimer les mots ayant moins de 3 caractères
    :return : le corpus final sous forme d'une liste
    """
    corpus = load_corpus(corpus_path)
    if lowercase:
        corpus = get_lower(corpus)
    if del_ponctuation:
        corpus = delete_ponctuation(corpus)
    corpus = tokenize_word(corpus)
    if lemm:
        corpus = lemmatisation(corpus)
    if del_stopwords:
        corpus = delete_stopwords(corpus)
    if rmv_words_less_than_3_chars:
        corpus = remove_words_less_than_3_chars(corpus)

    return corpus

def write_final_corpus(corpus, output_path):
    """
    Cette fonction fait appel au model word2vec dans le package tools
    Elle permet de reformer le texte traité et l'écrire dans fichier texte de sortie
    :param corpus:
    :param output_path:
    :return:
    """
    final_text = reform_text(corpus)
    write_corpus(final_text, output_path)

def similar_terms(model_path, terms_path, result_path):
    get_similar_terms(model_path, terms_path, result_path)

def similarities_to_list(file_similarities_path):
    return file_similarities_to_list(file_similarities_path)

def similar_terms_untrained_model(corpus, vector_size, window):
    mod = get_model(corpus, vector_size, window)
    words = get_words(mod)
    return words

def print_words(words, output_words_path):
    output_words = open(output_words_path, "w", encoding='UTF-8')
    for word in words.key_to_index:
        output_words.write(str(word))
        output_words.write("\n")
    output_words.close()

def get_most_similar_word(words, output_similar_words_path):
    """
    Permet de récupérer les termes similaires et les saisir dans le fichier de sortie
    :param words:
    :param output_similar_words_path:
    """
    output_similar_words = open(output_similar_words_path, "w", encoding='UTF-8')
    for word in words.key_to_index:
        output_similar_words.write(str(word)+";")
        words_list = words.most_similar(word)
        cpt = 0
        for x in words_list:
            if cpt < (len(words_list)-1):
                output_similar_words.write(str(x[0])+", ")
            else:
                output_similar_words.write(str(x[0]))
            cpt = cpt + 1
        output_similar_words.write("\n")
    output_similar_words.close()

def get_similar_terms_for_theme_controller(model_path, themes_list_path, levels, result_path):
    """
    Permet de récupérer le nuage de mots d'une thématique et saisir dans le fichier de sortie
    :param model_path:
    :param themes_list:
    :param levels:
    :param result_path:
    """
    out_similar_words = open(result_path, "w", encoding='UTF-8')
    themes_list = prepare_terms_list(themes_list_path)
    for theme in themes_list:
        nuage_mot = get_similar_terms_for_theme(model_path, theme, levels)
        if len(nuage_mot) > 1:
            for i in range(len(nuage_mot)):
                if i == 0:
                    out_similar_words.write(theme.replace("_", " ").strip() + ";")
                elif i == (len(nuage_mot) - 1):
                    out_similar_words.write(str(nuage_mot[i]).replace("_", " ").strip() + "\n")
                else:
                    out_similar_words.write(str(nuage_mot[i]).replace("_", " ").strip() + ", ")
    out_similar_words.close()
    
    
    



def load_corpus(corpus_path):
    """
    :param corpus_path:
    :return: le corpus chargé
    """
    corpus_path = open(corpus_path, "r")
    lines = corpus_path.readlines()
    return lines

def write_corpus(corpus, output_file_path):
    output_corpus = open(output_file_path, "w", encoding='UTF-8')
    for sent in corpus:
        output_corpus.write(str(sent)+" ")
    output_corpus.close()


def file_similarities_to_list(file_similarities_path):
    """
    Cette fonction permet de parcourir un fichier contenant les similarités, récupérer le contenu et
    le renvoyer sous forme d'une liste
    :param file_similarities_path : chemin vers le fichier contenant les similarités
    :return : liste des similarités
    """
    similarities = open(file_similarities_path, "r", encoding='UTF-8')
    similarities_list = []
    lines = similarities.readlines()
    for line in lines:
        similarities_list.append(line.strip())
    return similarities_list

def get_lower(lines):
    """
    Permet de rendre le corpus en minuscule
    :param lines : liste des lignes d'un texte
    :return : corpus en minuscule
    """
    return [doc.lower() for doc in lines]

def delete_ponctuation(corpus):
    """
    :param corpus:
    :return: corpus sans la ponctuation
    """
    corpus_1 = [doc.replace("'", " ").replace('_', ' ').replace('-', ' ') for doc in corpus]
    ponctuations_list = list(string.punctuation)
    return ["".join([char for char in list(doc) if not (char in ponctuations_list)]) for doc in corpus_1]

def tokenize_word(corpus):
    """
    :param corpus:
    :return: le corpus tokenizé par mot
    """
    return [word_tokenize(doc) for doc in corpus]

def lemmatisation(corpus_tk):
    """
    :param corpus_tk:
    :return: corpus lemmatisé
    """
    lem = WordNetLemmatizer()
    corpus_lm = [[lem.lemmatize(tok) for tok in doc] for doc in corpus_tk]
    return corpus_lm

def delete_stopwords(corpus_lm):
    """
    :param corpus_lm:
    :return: le corpus sans les stopwords
    """
    stop_words = stopwords.words('french')
    return [[tok for tok in doc if not (tok in stop_words)] for doc in corpus_lm]

def remove_words_less_than_3_chars(corpus_sw):
    """
    :param corpus_sw:
    :return : corpus sans les mots ayant moins de 3 caractères
    """
    return [[mot for mot in doc if (len(mot) >= 3)] for doc in corpus_sw]

def reform_text(corpus_sw):
    """
    :param corpus_sw:
    :return: le corpus reformé
    """
    return [" ".join(doc) for doc in corpus_sw]

def get_model(corpus, vector_size, window):
    """
    :param corpus:
    :param vector_size:
    :param window:
    :return: le modèle entrainé
    """
    mod = Word2Vec(corpus, vector_size=vector_size, window=window)
    return mod

def get_words(mod):
    """
    :param model : le modèle que vous avez entraîné
    :return: liste des termes
    """
    words = mod.wv
    # return words.key_to_index
    return words

def prepare_terms_list(terms_path):
    """
    Permet de préparer la liste des termes : lecture du fichier, liaison avec des _ entre les différents mots d'un terme
    :param terms_path : chemin vers la liste des termes
    :return : liste des termes lue avec remplacement de « » par « _ »
    """
    terms_list = open(terms_path, "r", encoding='UTF-8')
    lines = terms_list.readlines()
    prepared_terms_list = []
    for line in lines:
        if line.strip().split(";")[0] not in prepared_terms_list:
            line = line.replace("’ ", "'").replace("' ", "'").replace(' ', '_')
            prepared_terms_list.append(str(line).strip().split(';')[0])
    return prepared_terms_list


def get_similar_terms(model_path, terms_path, result_path):
    """
    Permet à partir d'un modèle pré-entraîné et d'une liste de termes de chercher les termes similaires aux termes
    se trouvant dans la liste sélectionnée.
    :param model_path : chemin vers le modèle pré-entraîné
    :param terms_path : chemin vers la liste des termes
    :param result_path : chemin vers là où on veut sauvegarder les résultats
    """
    model = KeyedVectors.load_word2vec_format(model_path, binary=True, unicode_errors="ignore")
    terms_list = prepare_terms_list(terms_path)
    out_similar_words = open(result_path, "w", encoding='UTF-8')
    for term in terms_list:
        try:
            s_words = model.most_similar(term.strip())
            similar_words = ""
            for s_word in s_words:
                if similar_words == "":
                    similar_words = s_word[0].strip()
                else:
                    similar_words = similar_words + ", " + s_word[0].strip()
            out_similar_words.write(term.strip().replace('_', ' ') + ";" + similar_words.replace('_', ' ') + "\n")
        except:
            pass
    out_similar_words.close()


def get_similar_terms_for_themes_list(model_path, themes_list):
    """

    :param model_path:
    :param themes_list:
    :return:
    """
    model = KeyedVectors.load_word2vec_format(model_path, binary=True, unicode_errors="ignore")
    s_words = []
    for theme in themes_list:
        try:
            s_words_tmp = model.most_similar(theme.strip())
            s_words = s_words + s_words_tmp
        except:
            pass
    return s_words



def get_similar_terms_for_theme(model_path, theme, levels):
    """

    :param model_path:
    :param theme:
    :param levels:
    :return : liste des termes du niveau suivant de la recherche
    """
    themes_list = []
    themes_list.append(theme)
    for level in range(levels):
        s_words = get_similar_terms_for_themes_list(model_path, themes_list)
        for s_word in s_words:
            if s_word[0] not in themes_list:
                themes_list.append(s_word[0])
    return themes_list


