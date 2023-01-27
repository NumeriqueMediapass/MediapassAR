from django.shortcuts import render
from .forms import SignupForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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