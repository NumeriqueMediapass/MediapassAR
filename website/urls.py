from django.urls import path
from .views import acceuil, monCompte, password_change, editProfile, deleteProfile


urlpatterns = [
    path('', acceuil, name='acceuil'),
    path('monCompte/', monCompte, name='monCompte'),
    path('password_change/', password_change, name='password_change'),
    path('editProfile/', editProfile, name='editProfile'),
    path('deleteProfile/', deleteProfile, name='deleteProfile'),
]