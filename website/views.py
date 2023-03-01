from datetime import date, timedelta

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import User
from app import settings
from mediatheque.models import Animation, Reservation, Mediatheque
from website.forms import EditProfileForm, PasswordChangingForm, CalendarWidget
from django.contrib.auth.decorators import login_required


# Create your views here.

def accueil(request):
    # On récupère toutes les animations
    animations = Animation.objects.all().order_by('date')
    anim = Animation.objects.all()
    res = []
    tmp = 0
    form = CalendarWidget()

    for animation in animations:
        if date.today() <= animation.date < date.today() + timedelta(days=7):
            res.append(animation)
            tmp = res.count(animation)

    res = res[:5]

    return render(request, 'website/accueil.html', {'animations': res, 'form': form, 'anim': anim, 'tmp': tmp})


# Fonction qui affiche toute les animations
def animations(request):
    # On récupère toutes les animations
    animations = Animation.objects.all()
    animations = animations.order_by('date')
    animation = []
    for tmp in animations:
        if tmp.date > date.today():
            animation.append(tmp)
    return render(request, 'website/animations.html', {'animation': animation})


def monCompte(request):
    return render(request, 'website/monCompte.html')


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return redirect('monCompte')

    else:
        form = PasswordChangingForm(request.user)
    return render(request, 'website/password_change.html', {
        'form': form
    })


# Fonction qui modifie les données d'un utilisateur
def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        # Vérifie si le formulaire est valide
        if form.is_valid():
            user = form.save(commit=False)
            if user.username != request.user.username and User.objects.filter(username=user.username).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà utilisé")
                return redirect('editProfile')
            user.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('monCompte')
    else:
        form = EditProfileForm(instance=request.user)
    args = {'form': form}
    return render(request, 'website/account_change.html', args)


# Fonction qui supprime un utilisateur
def deleteProfile(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            user.delete()
            return redirect('acceuil')
    else:

        return render(request, 'website/delete_account.html')


def print_animations(request, id_anim):
    # On récupère l'animation
    animation = Animation.objects.get(id=id_anim)
    # On récupère les réservations pour l'utilisateur connecté
    reservations = Reservation.objects.filter(user=request.user, animation_id=id_anim)
    print(reservations)
    return render(request, 'website/inscriptionAtelier.html', {'animation': animation, 'reservations': reservations})


# Fonction qui inscrit un utilisateur a une animation
def inscription(request):
    # On récupère l'utilisateur connecté
    user = request.user
    # On récupère l'animation
    animation = request.POST.get('animation')
    # On récupère la médiathèque
    mediatheque = request.POST.get('mediatheque')
    tmp = Mediatheque.objects.get(id=mediatheque)
    # On récupère le nombre de personne
    nb_person = request.POST.get('nb_person')
    # On vérifie si l'utilisateur est déjà inscrit
    if Reservation.objects.filter(user=user, animation=animation).exists():
        messages.error(request, "Vous êtes déjà inscrit à cette animation")
        return redirect('acceuil')
    # On inscrit l'utilisateur à l'animation
    reservation = Reservation(user=user, animation_id=animation,
                              mediatheque=tmp, nb_person=nb_person)
    reservation.save()
    # On envoie un mail a la médiathèque pour prévenir qu'un utilisateur s'est inscrit
    subject = "Inscription à une animation"
    message = "L'utilisateur " + user.username + " s'est inscrit à l'animation " + \
              Animation.objects.get(id=animation).name
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.mediatheque.email]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('acceuil')


# Fonction qui permet de voir les animations auxquelles l'utilisateur est inscrit
def mesReservations(request):
    # On récupère l'utilisateur connecté
    user = request.user
    # On récupère toutes les réservations de l'utilisateur
    reservations = Reservation.objects.filter(user=user)
    animations = []
    for reservation in reservations:
        animations.append(reservation.animation)
    return render(request, 'website/mesReservations.html', {'animations': animations})


# Fonction qui affiche l'animation sélectionnée
def animation(request, id):
    # On récupère l'animation
    animation = Animation.objects.get(id=id)
    return render(request, 'website/printAtelier.html', {'animation': animation})


# Fonction qui permet de supprimer une réservation
def deleteReservation(request, id):
    # On récupère l'utilisateur connecté
    user = request.user
    # On récupère la réservation
    reservation = Reservation.objects.get(animation_id=id, user_id=user.id)
    # On vérifie si l'utilisateur est bien celui qui a fait la réservation
    if user == reservation.user:
        reservation.delete()
    return redirect('mesReservations')
