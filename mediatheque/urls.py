from django.urls import path
from django.conf.urls.static import static

from app import settings
from . import views
from .views import print_atelier, add_atelier, edit_atelier, delete_atelier, get_inscription, print_animation, \
    confirm_inscription

urlpatterns = [
    path('mediatheque/index.html', views.index, name='index_mediatheque'),
    path('mediatheque/atelier.html', print_atelier, name='print_atelier'),
    path('mediatheque/add_atelier.html', add_atelier, name='add_atelier'),
    path('mediatheque/edit_atelier/<int:id>', edit_atelier, name='edit_atelier'),
    path('mediatheque/delete_atelier.html', delete_atelier, name='delete_atelier'),
    path('mediatheque/confirm_inscription/<int:id>', get_inscription, name='get_inscription'),
    path('mediatheque/list_animation.html', print_animation, name='print_animation'),
    path('mediatheque/confirm_inscription/', confirm_inscription, name='confirm_inscription'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)