# views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .tools import tool_load_file,tool_ENs
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
    if request.FILES.get('corpus'):

            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)
            tool_ENs.get_named_entities('data/'+fichier.name,'workspace/pers.csv','workspace/org.csv')

    return render(request,'pel_mel/en.html',{})





