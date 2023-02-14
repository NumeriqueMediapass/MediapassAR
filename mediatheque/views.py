from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.admin import User
from mediatheque.forms import AnimationForm, AnimationUpdateForm
from mediatheque.models import Animation, Reservation, Mediatheque


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


# Fonction qui permet de récupérer les reservations d'un utilisateur
def get_inscription(request, id):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    else:
        # On récupère l'atelier
        animation = Animation.objects.get(id=id)
        # On récupère les réservations de l'animation
        reservations = Reservation.objects.filter(animation=animation)

        return render(request, 'mediatheque/confirm_inscription.html', {'animation': animation, 'reservations': reservations})

# Fonction qui permet de confirmer l'inscription d'un utilisateur à une animation de notre médiathèque
def confirm_inscription(request):
    # On récupère l'animation et l'utilisateur
    id = request.POST.get('animation_id')
    animation = Animation.objects.get(id=id)
    user = User.objects.get(id=request.POST.get('user_id'))
    # On récupère la réservation de l'utilisateur pour l'animation
    reservation = Reservation.objects.get(animation_id=animation, user_id=user)
    # On vérifie que la variable Validated n'est pas déjà a True
    if not reservation.Validated:
        # On change la valeur de la variable validated
        reservation.Validated = True
        # On sauvegarde la réservation
        reservation.save()
    return redirect('get_inscription', id=id)


def print_animation(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    else:
        # On récupère les animations de la médiathèque de l'utilisateur
        mediatheques = Mediatheque.objects.get(user=request.user)
        animations = Animation.objects.filter(users_id=request.user)
        return render(request, 'mediatheque/list_animation.html',
                      {'mediatheques': mediatheques, 'animations': animations})