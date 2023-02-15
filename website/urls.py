from django.urls import path
from .views import acceuil, monCompte, password_change, editProfile, deleteProfile , inscription, \
    mesReservations, animation, deleteReservation


urlpatterns = [
    path('', acceuil, name='acceuil'),
    path('monCompte/', monCompte, name='monCompte'),
    path('password_change/', password_change, name='password_change'),
    path('editProfile/', editProfile, name='editProfile'),
    path('deleteProfile/', deleteProfile, name='deleteProfile'),
    path('inscription/', inscription, name='inscription'),
    path('mesReservations/', mesReservations, name='mesReservations'),
    path('animation/<int:id>', animation, name='animation'),
    path('deleteReservation/<int:id>', deleteReservation, name='deleteReservation'),
]