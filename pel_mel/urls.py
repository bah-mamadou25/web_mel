from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("en/", views.en, name="en"),
]