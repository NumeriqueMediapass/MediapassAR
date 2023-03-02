from django.urls import path
from .views import accueil, monCompte, ChangePassword, editProfile, deleteProfile, Signup, \
    mesReservations, animation, deleteReservation, AnimationsViews, animations

urlpatterns = [
    path('', accueil, name='acceuil'),
    path('monCompte/', monCompte, name='monCompte'),
    path('password_change/', ChangePassword, name='ChangePassword'),
    path('editProfile/', editProfile, name='editProfile'),
    path('deleteProfile/', deleteProfile, name='deleteProfile'),
    path('inscription/', Signup, name='Signup'),
    path('mesReservations/', mesReservations, name='mesReservations'),
    path('animation/<int:idanimations>', animation, name='animation'),
    path('deleteReservation/<int:idanimations>', deleteReservation, name='deleteReservation'),
    path('print_animations/<int:id_anim>', AnimationsViews, name='AnimationsViews'),
    path('animations/', animations, name='animations'),
]
