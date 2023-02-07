from django.urls import path

from . import views

urlpatterns = [
    path('mediatheque/index.html', views.index, name='index_mediatheque'),
    ]