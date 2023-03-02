from django.urls import path
from django.conf.urls.static import static

from app import settings
from . import views
from .views import AtelierViews, AddAtelier, AtelierEditing, AtelierDelation, InscriptionGet, AnimationViews, \
    SignupConfirm, SignupDeleting

urlpatterns = [
    path('mediatheque/index.html', views.index, name='index_mediatheque'),
    path('mediatheque/atelier.html', AtelierViews, name='AtelierViews'),
    path('mediatheque/AddAtelier.html', AddAtelier, name='AddAtelier'),
    path('mediatheque/edit_atelier/<int:id>', AtelierEditing, name='AtelierEditing'),
    path('mediatheque/delete_atelier.html', AtelierDelation, name='AtelierDelation'),
    path('mediatheque/confirm_inscription/<int:id>', InscriptionGet, name='InscriptionGet'),
    path('mediatheque/AnimationList.html', AnimationViews, name='AnimationViews'),
    path('mediatheque/confirm_inscription/', SignupConfirm, name='SignupConfirm'),
    path('mediatheque/delete_inscription/', SignupDeleting, name='SignupDeleting'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)