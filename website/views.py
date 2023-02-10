from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.admin import User

from mediatheque.models import Animation
from website.forms import EditProfileForm, PasswordChangingForm

# Create your views here.

def acceuil(request):
    return render(request, 'website/accueil.html')

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

# On récupère toutes les animations
def print_atelier(request):
    animations = Animation.objects.all()
    return render(request, 'website/accueil.html', {'animations': animations})