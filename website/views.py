from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import User

from mediatheque.models import Animation, Reservation, Mediatheque
from website.forms import EditProfileForm, PasswordChangingForm

# Create your views here.

def acceuil(request):
    # On récupère toutes les animations
    animations = Animation.objects.all()
    # On récupère toutes les réservations
    reservations = Reservation.objects.all()
    # On transforme les réservations en liste d'id d'utilisateur
    reservation = []
    for res in reservations:
        reservation.append(res.user.id)
    print('reservations : ', reservation)
    # On récupère l'utilisateur
    user = request.user
    return render(request, 'website/accueil.html', {'animations': animations, 'reservation': reservation
                                                    , 'user': user})

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


#fonction qui modifie les données d'un utilisateur
def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        #Vérifie si le formulaire est valide
        if form.is_valid():
            #Vérifie si le nom d'utilisateur est déjà utilisé
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà utilisé")
                return redirect('editProfile')
            form.save()
            return redirect('monCompte')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'website/account_change.html', args)


#Fonction qui supprime un utilisateur
def deleteProfile(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            user.delete()
            return redirect('acceuil')
    else:
 
        return render(request, 'website/delete_account.html')

# Fonction qui inscrit un utilisateur a une animation
def inscription(request):
    # On récupère l'utilisateur connecté
    user = request.user
    # On récupère l'animation
    animation = request.POST.get('atelier')
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
    reservation = Reservation(user=user, animation=Animation.objects.get(id=animation),
                              mediatheque=tmp, nb_person=nb_person)
    reservation.save()
    return redirect('acceuil')

