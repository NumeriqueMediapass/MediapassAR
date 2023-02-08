from django.urls import path
from django.conf.urls.static import static

from app import settings
from . import views
from .views import print_atelier, add_atelier

urlpatterns = [
    path('mediatheque/index.html', views.index, name='index_mediatheque'),
    path('mediatheque/atelier.html', print_atelier, name='print_atelier'),
    path('mediatheque/add_atelier.html', add_atelier, name='add_atelier'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)