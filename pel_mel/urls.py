from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("en/", views.en, name="en"),
    path("enapi/", views.enAPI, name="enAPI"),
    path("termes/",views.termes,name="termes"),
    path("termesAPI/", views.termesAPI, name="termesAPI"),
    path("relations/",views.relations,name="relations"),
]