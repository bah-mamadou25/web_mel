import os
import shutil

def workspace_path(request):
    workspace_path = "./workspaces/"+request.session.get('username')+"/"
    return workspace_path



def delete_workspace(directory_path):
    """
    Supprime le répertoire spécifié ainsi que son contenu (y compris les sous-répertoires et les fichiers).
    """
    shutil.rmtree(directory_path)
    
    
def create_workspace(workspace_path):
    """
    Crée un répertoire et ses sous-répertoires.
    """
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
        os.makedirs(workspace_path+'/data')
        os.makedirs(workspace_path+'/workspace')
        os.makedirs(workspace_path+'/workspace/ENs')
        os.makedirs(workspace_path+'/workspace/termes')
        os.makedirs(workspace_path+'/workspace/word2vec')
        os.makedirs(workspace_path+'/workspace/doc2vec')
        
        
        
        
        
