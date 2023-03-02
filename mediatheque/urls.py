from django.urls import path
from django.conf.urls.static import static

from app import settings
from . import views
from .views import AtelierViews, AddAtelier, AtelierEditing, AtelierDelation, InscriptionGet, AnimationViews, \
    SignupConfirm, SignupDeleting

urlpatterns = [
    path('mediatheque/index.html', views.index, name='index_mediatheque'),
    path('mediatheque/atelier.html', AtelierViews, name='print_atelier'),
    path('mediatheque/add_atelier.html', AddAtelier, name='add_atelier'),
    path('mediatheque/edit_atelier/<int:id>', AtelierEditing, name='edit_atelier'),
    path('mediatheque/delete_atelier.html', AtelierDelation, name='delete_atelier'),
    path('mediatheque/confirm_inscription/<int:id>', InscriptionGet, name='get_inscription'),
    path('mediatheque/list_animation.html', AnimationViews, name='print_animation'),
    path('mediatheque/confirm_inscription/', SignupConfirm, name='confirm_inscription'),
    path('mediatheque/delete_inscription/', SignupDeleting, name='delete_inscription'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)