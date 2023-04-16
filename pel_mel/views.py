# views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe
from .tools import tool_load_file,tool_ENs,tool_termes
import time,os


# Create your views here.

def accueil(request):
    if request.method == 'POST':
        if request.FILES.get('zipFile'):
            fichier = request.FILES['zipFile']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)
            tool_load_file.extract_file('data/'+fichier.name)
            print(fichier.name)
            tool_load_file.createCorpus('data/'+fichier.name,'workspace/corpus.txt')
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

