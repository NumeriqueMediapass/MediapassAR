import datetime
from django.shortcuts import render
from django.conf import settings
from .forms import SignupForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
import logging

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #On set les valeurs rentré dans le formulaire pour créer l'utilisateur
            email=request.POST.get('email')
            username=request.POST.get('username')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            #envoie de mail ici
            try:
                #On vérifie que l'adresse mail de l'utilisateur n'est pas déjà utilisé
                if User.objects.filter(email=email).exists():
                    exception = Exception('Cette adresse mail est déjà utilisée')
                    raise exception
                #On vérifie que le username de l'utilisateur n'est pas déjà utilisé
                elif User.objects.filter(username=username).exists():
                    exception = Exception('Ce username est déjà utilisé')
                    raise exception
                else : 
                    user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                    send_mail(
                        'Inscription sur le site Media Pass Atelier',
                        'Bienvenue sur le site nous vous remercions de votre inscription '+username+ ' ! ',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
            except Exception as e:
                logging.error('Erreur lors de l\'envoie du courriel',e)
                return redirect('signup')
        return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'connexion/signup.html', {'form': form})


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
            error = "Nom d'utilisateur ou mot de passe incorrect"
            return render(request, 'connexion/connexion.html', {'error': error})
    return render(request, 'connexion/connexion.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')
        

def acceuil(request):
    return render(request, 'connexion/acceuil.html')