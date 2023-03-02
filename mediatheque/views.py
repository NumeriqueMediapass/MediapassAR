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
        return render(request, 'mediatheque/atelier.html', {'animations': animations})
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
        return redirect('AtelierViews')


@user_passes_test(is_staff_or_superuser)
def AtelierEditing(request, idanimations):
    animation = Animation.objects.get(id=idanimations)
    if request.method == 'POST':
        form = AnimationUpdateForm(request.POST, request.FILES, instance=animation)
        if form.is_valid():
            form.save()
            return redirect('AtelierViews')
    else:
        form = AnimationUpdateForm(instance=animation)
    return render(request, 'mediatheque/AtelierEditing.html', {'form': form})


# Fonction qui permet de récupérer les reservations d'un utilisateur
@user_passes_test(is_staff_or_superuser)
def InscriptionGet(request, idanimations):
    # On récupère l'atelier
    animation = Animation.objects.get(id=idanimations)
    # On récupère les réservations de l'animation
    reservations = Reservation.objects.filter(animation=animation)

    return render(request, 'mediatheque/SignupConfirm.html',
                  {'animation': animation, 'reservations': reservations})


# Fonction qui permet de confirmer l'inscription d'un utilisateur à une animation de notre médiathèque
def SignupConfirm(request):
    # On récupère l'utilisateur
    id_user = request.POST.get('user_id')
    # On récupère l'animation et l'utilisateur
    animation = Animation.objects.get(id=request.POST.get('anim_id'))
    # On récupère la réservation de l'utilisateur pour l'animation
    reservation = Reservation.objects.get(animation_id=animation, user_id=id_user)
    # On vérifie que la variable Validated n'est pas déjà a True
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
    return redirect('InscriptionGet', id=animation.id)


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
    return redirect('InscriptionGet', id=animation.id)


# Fonction qui permet de récupérer les animations de la médiathèque de l'utilisateur
@user_passes_test(is_staff_or_superuser)
def AnimationViews(request):
    # On récupère les animations de la médiathèque de l'utilisateur
    mediatheques = Mediatheque.objects.get(user=request.user)
    animations = Animation.objects.filter(users_id=request.user)
    return render(request,
                  'mediatheque/AnimationList.html', {'mediatheques': mediatheques, 'animations': animations})
