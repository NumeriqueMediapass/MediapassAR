from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from app import settings
from mediatheque.forms import AnimationForm, AnimationUpdateForm
from mediatheque.models import Animation, Reservation, Mediatheque


# Create your views here.


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_staff_or_superuser)
def index(request):
    # On récupère les animations de la médiathèque
    animations = Animation.objects.filter(users_id=request.user)
    # On récupère la médiathèque de l'utilisateur
    mediatheque = Mediatheque.objects.get(user_id=request.user)
    return render(request, 'mediatheque/index.html', {'animations': animations, 'mediatheque': mediatheque})


@user_passes_test(is_staff_or_superuser)
def AtelierViews(request):
    # On regarde si l'utilisateur est un admin
    if request.user.is_superuser:
        # On récupère toutes les animations
        animations = Animation.objects.all()
        mediatheque = Mediatheque.objects.get(user_id=request.user)
        return render(request, 'mediatheque/atelier.html', {'animations': animations, 'mediatheque': mediatheque})
    # On regarde si l'utilisateur est un staff
    elif request.user.is_staff:
        # On récupère les animations de la médiathèque de l'utilisateur
        animations = Animation.objects.filter(users_id=request.user)
        mediatheque = Mediatheque.objects.get(user_id=request.user)
        return render(request, 'mediatheque/atelier.html', {'animations': animations, 'mediatheque': mediatheque})


@user_passes_test(is_staff_or_superuser)
def AddAtelier(request):
    if request.method == 'POST':
        form = AnimationForm(request.POST, request.FILES)
        if form.is_valid():
            animation = form.save(commit=False)
            animation.users = request.user
            animation.save()
            messages.success(request, 'L\'animation a bien été ajoutée')
            return redirect('AtelierViews')
    else:
        form = AnimationForm()
    return render(request, 'mediatheque/AddAtelier.html', {'form': form})


@user_passes_test(is_staff_or_superuser)
def AtelierDelation(request):
    if request.method == 'POST':
        # On récupère les id des utilisateurs à supprimer dans les checkbox cochées
        id_animations = request.POST.getlist('atelier')
        for id_animation in id_animations:
            Animation.objects.get(id=id_animation).delete()
        messages.success(request, 'L\'animation a bien été supprimée')
        return redirect('AtelierViews')


@user_passes_test(is_staff_or_superuser)
def AtelierEditing(request, idanimations):
    animation = Animation.objects.get(id=idanimations)
    if request.method == 'POST':
        form = AnimationUpdateForm(request.POST, request.FILES, instance=animation)
        if form.is_valid():
            form.save()
            messages.success(request, 'L\'animation a bien été modifié')
            return redirect('AtelierViews')
    else:
        form = AnimationUpdateForm(instance=animation)
    return render(request, 'mediatheque/AtelierEditing.html', {'form': form})


# Fonction qui permet de récupérer les reservations d'un utilisateur
@user_passes_test(is_staff_or_superuser)
def InscriptionGet(request, idanimation):
    # On récupère l'atelier
    animation = Animation.objects.get(id=idanimation)
    # On récupère les réservations de l'animation
    reservations = Reservation.objects.filter(animation=animation)
    reservation_validated = Reservation.objects.filter(animation=animation, Validated=True)
    # On récupère le nb_person de chaque reservation validé
    nb_person = 0
    for reservation in reservation_validated:
        nb_person += reservation.nb_person
    # On récupère le nb_person_max de l'animation
    nb_person_max = animation.nb_places
    # On récupère le nb_person restant
    nb_person_rest = nb_person_max - nb_person
    return render(request, 'mediatheque/SignupConfirm.html',
                  {'animation': animation, 'reservations': reservations, 'nb_person_rest': nb_person_rest})


# Fonction qui permet de confirmer l'inscription d'un utilisateur à une animation de notre médiathèque
def SignupConfirm(request):
    # On récupère l'utilisateur
    id_user = request.POST.get('user_id')
    # On récupère l'animation et l'utilisateur
    animation = Animation.objects.get(id=request.POST.get('anim_id'))
    # On récupère la réservation de l'utilisateur pour l'animation
    reservation = Reservation.objects.get(animation_id=animation, user_id=id_user)
    # On vérifie que la variable Validated n'est pas déjà a True
    reservation_validated = Reservation.objects.filter(animation=animation, Validated=True)
    # On récupère le nb_person de chaque reservation validé
    nb_person = 0
    for reservation in reservation_validated:
        nb_person += reservation.nb_person
    # On récupère le nb_person_max de l'animation
    nb_person_max = animation.nb_places
    # On récupère le nb_person restant
    nb_person_rest = nb_person_max - nb_person
    # On vérifie que le nb_person restant est supérieur ou égal au nb_person de la réservation
    if nb_person_rest >= reservation.nb_person:
        if not reservation.Validated:
            # On change la valeur de la variable validated
            reservation.Validated = True
            # On sauvegarde la réservation
            reservation.save()
            # On envoie un mail à l'utilisateur pour lui dire que sa réservation a été validée
            subject = 'Confirmation de votre inscription à l\'atelier ' + animation.name
            message = 'Bonjour, \n\nVotre inscription à l\'atelier ' + animation.name + ' a été validée. ' \
                                                                                    '\n\nCordialement, ' \
                                                                                    '\n\nL\'équipe de la médiathèque'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [reservation.user.email]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'L\'inscription a bien été confirmée')
        return redirect('InscriptionGet', idanimation=animation.id)
    else:
        messages.warning(request, 'Il n\'y a plus de place disponible pour cet atelier')
        return redirect('InscriptionGet', idanimation=animation.id)


# Fonction qui permet de supprimer l'inscription d'un utilisateur à une animation de notre médiathèque
def SignupDeleting(request):
    # On récupère l'animation et l'utilisateur
    animation = Animation.objects.get(id=request.POST.get('animation_id_supp'))
    # On récupère l'utilisateur
    user = request.POST.get('user_id_supp')
    # On récupère la réservation de l'utilisateur pour l'animation
    reservation = Reservation.objects.get(animation_id=animation, user_id=user)
    # On vérifie que la variable Validated est déjà à True
    if reservation.Validated:
        # On change la valeur de la variable validated
        reservation.Validated = False
        # On sauvegarde la réservation
        reservation.save()
        # On envoie un mail à l'utilisateur pour lui dire que sa réservation a été supprimée
        subject = 'Confirmation de votre inscription à l\'atelier ' + animation.name
        message = 'Bonjour, \n\nVotre inscription à l\'atelier ' + animation.name + ' a été supprimé. ' \
                                                                                    '\n\nCordialement, ' \
                                                                                    '\n\nL\'équipe de la médiathèque'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [reservation.user.email]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, 'L\'inscription a bien été supprimée')
    return redirect('InscriptionGet', idanimation=animation.id)


# Fonction qui permet de récupérer les animations de la médiathèque de l'utilisateur
@user_passes_test(is_staff_or_superuser)
def AnimationViews(request):
    # On récupère les animations de la médiathèque de l'utilisateur
    mediatheques = Mediatheque.objects.get(user=request.user)
    animations = Animation.objects.filter(users_id=request.user)
    return render(request,
                  'mediatheque/AnimationList.html', {'mediatheques': mediatheques, 'animations': animations})
