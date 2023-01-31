from django.urls import path
from .views import acceuil, monCompte


urlpatterns = [
    path('', acceuil, name='acceuil'),
    path('monCompte/', monCompte, name='monCompte'),
]