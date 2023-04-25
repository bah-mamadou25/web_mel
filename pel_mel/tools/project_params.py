
def workspace_path(request):
    workspace_path = "./workspaces/"+request.session.get('username')+"/"
    return workspace_path