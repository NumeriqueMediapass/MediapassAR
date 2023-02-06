from django.contrib.auth.models import User
from django.shortcuts import render,redirect

# Create your views here.

def index(request):
    return render(request, 'administration/index.html')

#fonction pour afficher les utilisateurs de la base de données
def print_users(request):
    #On récupère tous les utilisateurs de la base de données
    users = User.objects.all()
    #On les affiche dans la page users.html
    return render(request, 'administration/users.html', {'users': users})