# views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .controllers import controller_load_file
import time,os


# Create your views here.

def accueil(request):
    if request.method == 'POST' and request.FILES['zipFile']:
        
        fichier = request.FILES['zipFile']
        fs = FileSystemStorage()
        nom_fichier = fs.save('data/'+fichier.name, fichier)
        controller_load_file.extract_file('data/'+fichier.name)
        controller_load_file.createCorpus('data/messages_presse','workspace/corpus.txt')
        return controller_load_file.download_corpus("workspace/corpus.txt")
        

    return render(request,'pel_mel/index.html',{})





