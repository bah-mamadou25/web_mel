from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path("", views.connex, name="connex"),
    path("accueil/", views.accueil, name="accueil"),
    path("en/", views.en, name="en"),
    path("enapi/", views.enAPI, name="enAPI"),
    path("termes/",views.termes,name="termes"),
    path("termesAPI/", views.termesAPI, name="termesAPI"),
    path("relations/",views.relations,name="relations"),
    path("relationsAPI/",views.relationsAPI,name="relationsAPI"),
    path("word2vec/",views.word2vec,name="word2vec"),
    path("trainAPI/",views.trainAPI,name="trainAPI"),
    path("useTermesAPI/",views.useTermesAPI,name="useTermesAPI"),
    path("thematiqueAPI/",views.thematiqueAPI,name="thematiqueAPI"),
    path("doc2vec/",views.doc2vec,name="doc2vec"),
     path("validationen/",views.validationEn, name="validationen")
    
]