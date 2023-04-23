# views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from .tools import tool_load_file,tool_ENs,tool_termes,tool_relationsPatterns,tool_word2vec
import time,os


# Create your views here.

def accueil(request):
    if request.method == 'POST':
        if request.FILES.get('zipFile'):
            fichier = request.FILES['zipFile']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)
            tool_load_file.extract_file('data/'+fichier.name)
            
            tool_load_file.createCorpus( os.path.splitext('data/'+fichier.name)[0],'workspace/corpus.txt')
            print(os.path.splitext('data/'+fichier.name)[0])
            return tool_load_file.download_corpus("workspace/corpus.txt")
        
        elif request.FILES.get('corpus'):

            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)
           
            tool_load_file.cleanUpCorpus('data/'+fichier.name,'workspace/cleaned_'+fichier.name)
            if 'toSplit' in request.POST:
                tool_load_file.retrieveSentences('workspace/cleaned_'+fichier.name)
                return tool_load_file.download_directory_as_zip('workspace')
            else:
                return tool_load_file.download_corpus('workspace/cleaned_'+fichier.name)

    return render(request,'pel_mel/index.html',{})

def en(request):
    table_personnes=''
    table_organisations=''
    if request.FILES.get('corpus'):
            
            tool_ENs.create_dir('workspace/ENs')
            tool_ENs.create_dir('data')
            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)    
            tool_ENs.get_named_entities('data/'+fichier.name,'workspace/ENs/pers.csv','workspace/ENs/org.csv')

            if os.path.exists("data/bulky"):
                tool_ENs.fusion_files("workspace/ENs","pers.csv","workspace/ENs/pers.csv")
                tool_ENs.fusion_files("workspace/ENs","org.csv","workspace/ENs/org.csv")

            table_personnes=tool_ENs.csv_to_html_table('workspace/ENs/pers.csv') 
            table_organisations=tool_ENs.csv_to_html_table('workspace/ENs/org.csv') 
    return render(request,'pel_mel/en.html',{'table_personnes': mark_safe(table_personnes), 'table_organisations': mark_safe(table_organisations),})
    




def termes(request):
     termes=''
     if request.FILES.get('corpus'):      
        tool_ENs.create_dir('data')
        tool_ENs.create_dir('workspace/termes')
        fichier = request.FILES['corpus']
        stem="False"
        fs = FileSystemStorage()
        fs.save('data/'+fichier.name, fichier)  
        if request.POST.get('reduire'):
            stem="True"         
               
        methodeScoring = request.POST['methodeScoring']
        minimum=request.POST['min']
        maximum=request.POST['max']
        tool_termes.terms_extraction('data/'+fichier.name,'workspace/termes/termes.csv',stem,methodeScoring,minimum,maximum)
        if os.path.exists("data/bulky"):
            tool_ENs.fusion_files("workspace/termes","termes.csv","workspace/termes/termes.csv")            

        termes=tool_ENs.csv_to_html_table('workspace/termes/termes.csv') 
      
     return render(request,'pel_mel/termes.html',{'termes':mark_safe(termes)})



def relations(request):
     nb_relations=0
     table_relations=''
     patterns=sorted(tool_relationsPatterns.get_patterns('patterns.txt'))
     if request.method == 'POST':
        tool_ENs.create_dir('workspace/relations')
        tool_ENs.create_dir('data')
        corpus = request.FILES['corpus']
        fs = FileSystemStorage()
        fs.save('data/'+corpus.name, corpus)   
        termes = request.FILES['termes']
        fs = FileSystemStorage()
        fs.save('data/'+termes.name, termes) 
        
        selected_patterns = request.POST.getlist('selected_patterns')
        rel_selected=', '.join(tool_relationsPatterns.get_relations_from_patterns(selected_patterns))
        print("before")
        tool_relationsPatterns.getRelations(selected_patterns, 'data/'+corpus.name, 'data/'+termes.name, rel_selected, 'workspace/relations/relations.csv')
        print("after")
        table_relations=tool_ENs.csv_to_html_table('workspace/relations/relations.csv') 
        nb_relations=tool_termes.get_number_of_sentences('workspace/relations/relations.csv')
     return render(request,'pel_mel/relations.html',{'patterns':patterns,'nb_relations': nb_relations,'table_relations': mark_safe(table_relations)})
 
def word2vec(request):
    if request.method == 'POST':
        
        if request.FILES.get('corpus'):
            tool_ENs.create_dir('workspace/word2vec')
            tool_ENs.create_dir('data')
            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)
            tool_load_file.extract_file('data/'+fichier.name)
            lowercase=False
            ponctuation=False
            lemm=False
            del_mt_words=False
            rmv_words_less_than_3_chars=False
            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)
            if request.POST.get('lowerCase'):
                lowercase=True 
            if request.POST.get('ponctuation'):
                ponctuation=True
            if request.POST.get('lemm'):
                lemm=True 
            if request.POST.get('vide'):
                del_mt_words=True
            if request.POST.get('troisChar'):
                rmv_words_less_than_3_chars=True

            corpus_traite=tool_word2vec.preprocessing_word2vec('data/'+fichier.name,lowercase,ponctuation,lemm,del_mt_words,rmv_words_less_than_3_chars)
            tool_word2vec.write_final_corpus(corpus_traite,'workspace/word2vec/corpus_traite.txt')
            return tool_load_file.download_corpus('workspace/word2vec/corpus_traite.txt')
    return render(request,'pel_mel/word2vec.html',{})






############################### API RESPONSE 

def enAPI(request):
    table_personnes=''
    table_organisations=''       
    if request.FILES.get('corpus'):
        tool_ENs.create_dir('workspace/ENs')
        tool_ENs.create_dir('data')
        fichier = request.FILES['corpus']
        fs = FileSystemStorage()
        fs.save('data/'+fichier.name, fichier)
        tool_ENs.get_named_entities('data/'+fichier.name, 'workspace/ENs/pers.csv', 'workspace/ENs/org.csv')

        if os.path.exists("data/bulky"):
            tool_ENs.fusion_files("workspace/ENs","pers.csv","workspace/ENs/pers.csv")
            tool_ENs.fusion_files("workspace/ENs","org.csv","workspace/ENs/org.csv")

        table_personnes = tool_ENs.csv_to_html_table('workspace/ENs/pers.csv')
        table_organisations = tool_ENs.csv_to_html_table('workspace/ENs/org.csv')

    data = {
            'table_personnes': table_personnes,
            'table_organisations': table_organisations,
        }   
    
    return JsonResponse(data)

def termesAPI(request):
     termes=''
     if request.FILES.get('corpus'):      
        tool_ENs.create_dir('data')
        tool_ENs.create_dir('workspace/termes')
        fichier = request.FILES['corpus']
        stem="False"
        fs = FileSystemStorage()
        fs.save('data/'+fichier.name, fichier)  
        if request.POST.get('reduire'):
            stem="True"         
               
        methodeScoring = request.POST['methodeScoring']
        minimum=request.POST['min']
        maximum=request.POST['max']
        tool_termes.terms_extraction('data/'+fichier.name,'workspace/termes/termes.csv',stem,methodeScoring,minimum,maximum)
        if os.path.exists("data/bulky"):
            tool_ENs.fusion_files("workspace/termes","termes.csv","workspace/termes/termes.csv")            

        termes=tool_ENs.csv_to_html_table('workspace/termes/termes.csv') 
        data = {
            'termes': termes
        } 
      
     return JsonResponse(data)