# views.py
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from .tools import tool_load_file,tool_ENs,tool_termes,tool_relationsPatterns,tool_word2vec,project_params,tool_doc2vec
import time,os
from .models import User

# Create your views here.
def connex(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            
        if user and user.check_password(password):
            request.session['username'] = username
            return redirect('accueil')
        else:
            message = 'Nom d\'utilisateur ou mot de passe invalide.'
    else:
        message = None
        
    return render(request, 'pel_mel/log.html', {'message': message})
    

def accueil(request):
    if request.method == 'POST':
        if request.FILES.get('zipFile'):
            fichier = request.FILES['zipFile']
            fs = FileSystemStorage()
            fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)
            tool_load_file.extract_file(project_params.workspace_path(request)+'data/'+fichier.name)
            
            tool_load_file.createCorpus( os.path.splitext(project_params.workspace_path(request)+'data/'+fichier.name)[0],project_params.workspace_path(request)+'workspace/corpus.txt')
            print(os.path.splitext(project_params.workspace_path(request)+'data/'+fichier.name)[0])
            return tool_load_file.download_corpus(project_params.workspace_path(request)+"workspace/corpus.txt")
        
        elif request.FILES.get('corpus'):

            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)
           
            tool_load_file.cleanUpCorpus(project_params.workspace_path(request)+'data/'+fichier.name,project_params.workspace_path(request)+'workspace/cleaned_'+fichier.name)
            if 'toSplit' in request.POST:
                tool_load_file.retrieveSentences(project_params.workspace_path(request)+'workspace/cleaned_'+fichier.name)
                return tool_load_file.download_directory_as_zip(project_params.workspace_path(request)+'workspace')
            else:
                return tool_load_file.download_corpus(project_params.workspace_path(request)+'workspace/cleaned_'+fichier.name)

    return render(request,'pel_mel/index.html',{})

def en(request):

    table_personnes=''
    table_organisations=''
    if request.FILES.get('corpus'):
            print(project_params.workspace_path(request)+'workspace/ENs')
            tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/ENs')
            tool_ENs.create_dir(project_params.workspace_path(request)+'data')
            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier) 
               
            tool_ENs.get_named_entities(request,project_params.workspace_path(request)+'data/'+fichier.name,
                                        project_params.workspace_path(request)+'workspace/ENs/pers.csv',
                                        project_params.workspace_path(request)+'workspace/ENs/org.csv')

            if os.path.exists(project_params.workspace_path(request)+"data/bulky"):
                tool_ENs.fusion_files(project_params.workspace_path(request)+"workspace/ENs","pers.csv",
                                      project_params.workspace_path(request)+"workspace/ENs/pers.csv")
                tool_ENs.fusion_files(project_params.workspace_path(request)+"workspace/ENs","org.csv",
                                      project_params.workspace_path(request)+"workspace/ENs/org.csv")

            table_personnes=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/ENs/pers.csv') 
            table_organisations=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/ENs/org.csv') 
            
    return render(request,'pel_mel/en.html',{'table_personnes': mark_safe(table_personnes), 'table_organisations': mark_safe(table_organisations),})
    
def validationEn(request):
    table_personnes=''
    table_personnes=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/ENs/pers.csv')
    return render(request,'pel_mel/validationen.html',context={'table_personnes':mark_safe(table_personnes)})




def termes(request):
     termes=''
     if request.FILES.get('corpus'):      
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/termes')
        fichier = request.FILES['corpus']
        stem="False"
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)  
        if request.POST.get('reduire'):
            stem="True"         
               
        methodeScoring = request.POST['methodeScoring']
        minimum=request.POST['min']
        maximum=request.POST['max']
        tool_termes.terms_extraction(project_params.workspace_path(request)+'data/'+fichier.name,
                                     project_params.workspace_path(request)+'workspace/termes/termes.csv',stem,methodeScoring,minimum,maximum)
        if os.path.exists(project_params.workspace_path(request)+"data/bulky"):
            tool_ENs.fusion_files(project_params.workspace_path(request)+"workspace/termes","termes.csv",
                                  project_params.workspace_path(request)+"workspace/termes/termes.csv")            

        termes=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/termes/termes.csv') 
      
     return render(request,'pel_mel/termes.html',{'termes':mark_safe(termes)})



def relations(request):
     nb_relations=0
     table_relations=''
     patterns=sorted(tool_relationsPatterns.get_patterns('patterns.txt'))
     if request.method == 'POST':
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/relations')
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        corpus = request.FILES['corpus']
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+corpus.name, corpus)   
        termes = request.FILES['termes']
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+termes.name, termes) 
        
        selected_patterns = request.POST.getlist('selected_patterns')
        rel_selected=', '.join(tool_relationsPatterns.get_relations_from_patterns(selected_patterns))
        
        tool_relationsPatterns.getRelations(selected_patterns, project_params.workspace_path(request)+'data/'+corpus.name,project_params.workspace_path(request)+ 'data/'+termes.name, rel_selected, project_params.workspace_path(request)+'workspace/relations/relations.csv')
        
        table_relations=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/relations/relations.csv') 
        nb_relations=tool_termes.get_number_of_sentences(project_params.workspace_path(request)+'workspace/relations/relations.csv')
     return render(request,'pel_mel/relations.html',{'patterns':patterns,'nb_relations': nb_relations,'table_relations': mark_safe(table_relations)})
 
def word2vec(request):
    if request.method == 'POST':
        
        if request.FILES.get('corpus'):
            tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/word2vec')
            tool_ENs.create_dir(project_params.workspace_path(request)+'data')
            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save('data/'+fichier.name, fichier)
            tool_load_file.extract_file(project_params.workspace_path(request)+'data/'+fichier.name)
            lowercase=False
            ponctuation=False
            lemm=False
            del_mt_words=False
            rmv_words_less_than_3_chars=False
            fichier = request.FILES['corpus']
            fs = FileSystemStorage()
            fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)
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
            
            corpus_traite=tool_word2vec.preprocessing_word2vec(project_params.workspace_path(request)+'data/'+fichier.name,lowercase,ponctuation,lemm,del_mt_words,rmv_words_less_than_3_chars)
            tool_word2vec.save_phrases_to_csv(corpus_traite,project_params.workspace_path(request)+'workspace/word2vec/corpus_traite.csv')
            return tool_load_file.download_corpus(project_params.workspace_path(request)+'workspace/word2vec/corpus_traite.csv')
    return render(request,'pel_mel/word2vec.html',{})




def doc2vec(request):
    resultat=''
    tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/doc2vec')
    tool_ENs.create_dir(project_params.workspace_path(request)+'data')
            
    if request.method == 'POST':
        if request.FILES.get('thematiques') and request.FILES.get('corpus'):
            fichier_thems = request.FILES['thematiques']
            corpus = request.FILES['corpus']
            
            fs = FileSystemStorage()
            fs.save(project_params.workspace_path(request)+'data/'+fichier_thems.name, fichier_thems)
            fs.save(project_params.workspace_path(request)+'data/'+corpus.name, corpus)
            
            tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/doc2vec/thematique_plus_nuage_de_mots')
            
            pathTo=project_params.workspace_path(request)+'workspace/doc2vec/'
            tool_doc2vec.prepare_themes_for_doc2vec(project_params.workspace_path(request)+'data/'+corpus.name,
                                                    project_params.workspace_path(request)+'data/'+fichier_thems.name,
                                                    project_params.workspace_path(request)+'workspace/doc2vec/thematique_plus_nuage_de_mots')
            return tool_load_file.download_directory_as_zip( project_params.workspace_path(request)+'workspace/doc2vec/thematique_plus_nuage_de_mots')
        else :
            
            f_dir_messages=request.FILES.get('msgZip')
            f_dir_thems=request.FILES.get('thematiquesZip')
            f_thems1=request.FILES.get('thematique1')
            f_thems2=request.FILES.get('thematique2')
            f_thems3=request.FILES.get('thematique3')
            vector_size=request.POST['dimVec']
            cont_min=request.POST['freqMin']
            val_epochs=request.POST['epochs']
            
            
            fs = FileSystemStorage()
            fs.save(project_params.workspace_path(request)+'data/'+f_dir_messages.name, f_dir_messages)
            tool_load_file.extract_file(project_params.workspace_path(request)+'data/'+f_dir_messages.name)
            
            tool_ENs.create_dir(project_params.workspace_path(request)+'data/nuage_de_mots')
            fs.save(project_params.workspace_path(request)+'data/nuage_de_mots/'+f_dir_thems.name, f_dir_thems)
            tool_load_file.extract_file(project_params.workspace_path(request)+'data/nuage_de_mots/'+f_dir_thems.name)
            os.remove(project_params.workspace_path(request)+'data/nuage_de_mots/'+f_dir_thems.name)
            
            fs.save(project_params.workspace_path(request)+'data/'+f_thems1.name, f_thems1)
            fs.save(project_params.workspace_path(request)+'data/'+f_thems2.name, f_thems2)
            fs.save(project_params.workspace_path(request)+'data/'+f_thems3.name, f_thems3)
            
            
            
            
            
            
            
            
            
            rslt=tool_doc2vec.messages_presse_classification(os.path.splitext(project_params.workspace_path(request)+'data/'+f_dir_messages.name)[0],
                                                             project_params.workspace_path(request)+'data/nuage_de_mots',
                                                             project_params.workspace_path(request)+'data/'+f_thems1.name,
                                                             project_params.workspace_path(request)+'data/'+f_thems2.name,
                                                             project_params.workspace_path(request)+'data/'+f_thems3.name,
                                                             int(vector_size),int(cont_min),int(val_epochs),project_params.workspace_path(request)+'workspace/doc2vec/resultat.csv')

            
            resultat=tool_doc2vec.csv_no_header_to_html_table(project_params.workspace_path(request)+'workspace/doc2vec/resultat.csv')
            
    return render(request,'pel_mel/doc2vec.html',{'resultat': mark_safe(resultat)})




############################### API RESPONSE 

def enAPI(request):
    table_personnes=''
    table_organisations=''  
    
    if request.FILES.get('corpus'):
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/ENs')
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        fichier = request.FILES['corpus']
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)
        tool_ENs.get_named_entities(request,project_params.workspace_path(request)+'data/'+fichier.name, 
                                    project_params.workspace_path(request)+'workspace/ENs/pers.csv',
                                    project_params.workspace_path(request)+'workspace/ENs/org.csv')

        if os.path.exists(project_params.workspace_path(request)+"data/bulky"):
            tool_ENs.fusion_files(project_params.workspace_path(request)+"workspace/ENs","pers.csv",
                                  project_params.workspace_path(request)+"workspace/ENs/pers.csv")
            tool_ENs.fusion_files(project_params.workspace_path(request)+"workspace/ENs","org.csv",
                                  project_params.workspace_path(request)+"workspace/ENs/org.csv")

        table_personnes = tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/ENs/pers.csv')
        table_organisations = tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/ENs/org.csv')

    data = {
            'table_personnes': table_personnes,
            'table_organisations': table_organisations,
        }   
    
    return JsonResponse(data)

def termesAPI(request):
     termes=''
     if request.FILES.get('corpus'):      
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/termes')
        fichier = request.FILES['corpus']
        stem="False"
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)  
        if request.POST.get('reduire'):
            stem="True"         
               
        methodeScoring = request.POST['methodeScoring']
        minimum=request.POST['min']
        maximum=request.POST['max']
        tool_termes.terms_extraction(project_params.workspace_path(request)+'data/'+fichier.name,
                                     project_params.workspace_path(request)+'workspace/termes/termes.csv',stem,methodeScoring,minimum,maximum)
        
        if os.path.exists(project_params.workspace_path(request)+"data/bulky"):
            tool_ENs.fusion_files(project_params.workspace_path(request)+"workspace/termes","termes.csv",
                                  project_params.workspace_path(request)+"workspace/termes/termes.csv")            

        termes=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/termes/termes.csv') 
        data = {
            'termes': termes
        } 
      
     return JsonResponse(data)


def relationsAPI(request):
     table_relations=''
     if request.method == 'POST':
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/relations')
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        corpus = request.FILES['corpus']
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+corpus.name, corpus)   
        termes = request.FILES['termes']
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+termes.name, termes) 
        
        selected_patterns = request.POST.getlist('selected_patterns')
        rel_selected=', '.join(tool_relationsPatterns.get_relations_from_patterns(selected_patterns))
        
        tool_relationsPatterns.getRelations(selected_patterns, project_params.workspace_path(request)+'data/'+corpus.name,project_params.workspace_path(request)+ 'data/'+termes.name, rel_selected, project_params.workspace_path(request)+'workspace/relations/relations.csv')
        
        table_relations=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/relations/relations.csv') 
       
        
        data = {
            'table_relations': table_relations
        } 
        print(table_relations)
     return JsonResponse(data)








def trainAPI(request):
    termes=''
    if request.FILES.get('corpusTraite'):      
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/termes')
        fichier = request.FILES['corpusTraite']
        
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)  

        entry_label_vector_size = request.POST['mots']
        entry_label_window=request.POST['fenetre']
        list_sentences=tool_word2vec.read_csv_file_to_list_sentences(project_params.workspace_path(request)+'data/'+fichier.name)
        termes = tool_word2vec.similar_terms_untrained_model(list_sentences, int(entry_label_vector_size), int(entry_label_window))

        data = {
            'termes':  tool_ENs.vec_to_html_table(termes)
        } 
      
    return JsonResponse(data)


def useTermesAPI(request):
    termesSimilaires=''
    if request.FILES.get('corpusTermes'):      
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/word2vec')
        fichier = request.FILES['corpusTermes']
       
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)  

        tool_word2vec.similar_terms('word2vec_models/frWac_no_postag_phrase_500_cbow_cut100.bin',project_params.workspace_path(request)+'data/'+fichier.name,project_params.workspace_path(request)+'workspace/word2vec/termes_sim.csv')
        
        termesSimilaires=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/word2vec/termes_sim.csv')
        data = {
            'termesSimilaires' :termesSimilaires
        } 
      
    return JsonResponse(data)

def thematiqueAPI(request):
    thematiques=''
    if request.FILES.get('corpusThematique'):      
        tool_ENs.create_dir(project_params.workspace_path(request)+'data')
        tool_ENs.create_dir(project_params.workspace_path(request)+'workspace/word2vec')
        fichier = request.FILES['corpusThematique']
       
        fs = FileSystemStorage()
        fs.save(project_params.workspace_path(request)+'data/'+fichier.name, fichier)  
        deep=request.POST['profondeur']
        tool_word2vec.get_similar_terms_for_theme_controller('word2vec_models/frWac_no_postag_phrase_500_cbow_cut100.bin',
                                                             project_params.workspace_path(request)+'data/'+fichier.name,int(deep),
                                                             project_params.workspace_path(request)+'workspace/word2vec/thematiques_sim.csv')
    thematiques=tool_ENs.csv_to_html_table(project_params.workspace_path(request)+'workspace/word2vec/thematiques_sim.csv')   
    
    data = {
        'thematiques': thematiques  
    } 
      
    return JsonResponse(data)