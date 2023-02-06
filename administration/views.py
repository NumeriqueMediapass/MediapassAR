from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render,redirect

# Create your views here.

def index(request):
    return render(request, 'administration/index.html')

#fonction pour afficher les utilisateurs de la base de données
def print_users(request):
    #On récupère tous les utilisateurs de la base de données ainsi que leurs informations
    users = User.objects.all()
    #On les affiche dans la page users.html
    return render(request, 'administration/users.html', {'users': users})

#Fonction qui permet de modifier les informations d'un utilisateur
def edit_user(request, id):
    #On vérifie si le formulaire a été envoyé
    if request.method == 'POST':
        #On récupère l'utilisateur dont l'id est passé en paramètre
        user_info = User.objects.get(id=id)
        #On vérifie si le nom d'utilisateur est déjà utilisé
        if User.objects.filter(username=request.POST['username']).exists():
            #On affiche un message d'erreur
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé")
            #On redirige vers la page d'édition de l'utilisateur
            return redirect('edit_user', id=id)
        #On modifie les informations de l'utilisateur
        user_info.username = request.POST['username']
        user_info.email = request.POST['email']
        user_info.first_name = request.POST['first_name']
        user_info.last_name = request.POST['last_name']
        #On sauvegarde les modifications
        user_info.save()
        #On redirige vers la page des utilisateurs
        return redirect('print_users')
    #On récupère l'utilisateur dont l'id est passé en paramètre
    user_info = User.objects.get(id=id)
    context = {'user_info': user_info}
    #On affiche le formulaire d'édition de l'utilisateur
    return render(request, 'administration/edit_user.html', context)