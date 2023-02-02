from audioop import reverse
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from .forms import SignupForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
import logging
from django.contrib.auth.tokens import default_token_generator
from .models import Token
# Create your views here.

#Fonction pour s'enregistrer sur le site
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email=request.POST.get('email')
            username=request.POST.get('username')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            try:
                if User.objects.filter(email=email).exists():
                    exception = Exception('Cette adresse mail est déjà utilisée')
                    raise exception
                elif User.objects.filter(username=username).exists():
                    exception = Exception('Ce username est déjà utilisé')
                    raise exception
                else : 
                    user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name,is_active=False)
                    token = default_token_generator.make_token(user)
                    confirmation_url = reverse('confirm_signup', kwargs={'token': token})

                    #Création du message pour l'inscription
                    subject = 'Confirmation de votre inscription'
                    message = 'Bonjour {}, merci de confirmer votre inscription en cliquant sur le lien suivant : {}'.format(username, confirmation_url)
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                    #On ajoute dans la table token le username et le token
                    token = Token(username=username, token=token)
                    token.save()
                    
            except Exception as e:
                logging.error('Erreur lors de l\'envoie du courriel',e)
                return redirect('signup')
        return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'connexion/signup.html', {'form': form})


#Fonction qui confirme l'inscription au site
def confirm_signup(request, token):
# Vérification du token
    if request.method == 'POST':
        username = Token.objects.get(token=token).username
        user = User.objects.get(username=username)
        if user is not None:
            user.is_active = True
            user.save()
            #Supprimer le token de la table token
            Token.objects.filter(token=token).delete()
            return redirect('login')
        else:
            # Le token est invalide, tu lance un message d'erreur
            return render(request, 'account/confirm_signup_error.html')
    else:
        return render(request, 'connexion/confirm_signup.html', {'token': token})


#Fonction qui permet de se connecter au site
def login_view(request):
    error = None
    if request.method == 'POST':
        # Récupération des données d'identification de l'utilisateur
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentification de l'utilisateur
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            error = "Nom d'utilisateur ou mot de passe incorrect ou inscription non validée"
            return render(request, 'connexion/connexion.html', {'error': error})
    return render(request, 'connexion/connexion.html')


#Fonction qui permet de se déconnecter du site
def logout_view(request):
    logout(request)
    return redirect('/login/')
        
#Fonction qui permet d'accéder à la page d'accueil
def acceuil(request):
    if(request.user.is_active == False):
        return redirect('login')
    return render(request, 'connexion/acceuil.html')

#Fonction qui permet de réinitialiser le mot de passe
def reset_password(request):
    pass