from django.shortcuts import render, redirect

from mediatheque.forms import AnimationForm, AnimationUpdateForm
from mediatheque.models import Animation


# Create your views here.

def index(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil du site
        return redirect('acceuil')
    return render(request, 'mediatheque/index.html', {})

def print_atelier(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    else :
        # On regarde si l'utilisateur est un admin
        if request.user.is_superuser:
            # On récupère toutes les animations
            animations = Animation.objects.all()
            return render(request, 'mediatheque/atelier.html', {'animations': animations})
        # On regarde si l'utilisateur est un staff
        elif request.user.is_staff:
            # On récupère les animations de la médiathèque de l'utilisateur
            animations = Animation.objects.filter(mediatheque__user=request.user)
            return render(request, 'mediatheque/atelier.html', {'animations': animations})

def add_atelier(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    if request.method == 'POST':
        form = AnimationForm(request.POST, request.FILES)
        if form.is_valid():
            animation = form.save(commit=False)
            animation.users = request.user
            animation.save()
            return redirect('print_atelier')
    else:
        form = AnimationForm()
    return render(request, 'mediatheque/add_atelier.html', {'form': form})


def delete_atelier(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    if request.method == 'POST':
        # On récupère les id des utilisateurs à supprimer dans les checkbox cochées
        id_animations = request.POST.getlist('atelier')
        for id_animation in id_animations:
            Animation.objects.get(id=id_animation).delete()
        return redirect('print_atelier')


def edit_atelier(request, id):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    animation = Animation.objects.get(id=id)
    if request.method == 'POST':
        form = AnimationUpdateForm(request.POST, request.FILES, instance=animation)
        if form.is_valid():
            form.save()
            return redirect('print_atelier')
    else:
        form = AnimationUpdateForm(instance=animation)
    return render(request, 'mediatheque/edit_atelier.html', {'form': form})