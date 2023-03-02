
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
import logging

# Create your views here.

# Fonction pour s'enregistrer sur le site

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('acceuil')
    else:
        form = AuthenticationForm()
    return render(request, 'connexion/connexion.html', context={'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            try:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Cette adresse mail est déjà utilisée')
                    return redirect('signup')
                elif User.objects.filter(username=username).exists():
                    messages.error(request, 'Ce username est déjà utilisé')
                    return redirect('signup')
                else:
                    user = User.objects.UsersCreation(username=username, email=email, password=password1,
                                                      first_name=first_name, last_name=last_name)
                    # Envoi d'un email simple de confirmation
                    subject = 'Confirmation de votre inscription'
                    message = 'Bonjour {}, merci de vous être inscrit sur notre site.'.format(username)
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            except Exception as e:
                logging.error('Erreur lors de l\'envoi du courriel', e)
                messages.error(request, 'Une erreur s\'est produite, veuillez réessayer plus tard.')
                return redirect('signup')
        return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'connexion/signup.html', {'form': form})


# Fonction qui permet de se déconnecter du site
def logout_view(request):
    logout(request)
    return redirect('/login/')