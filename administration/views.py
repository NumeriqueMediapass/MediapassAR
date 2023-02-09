from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from administration.forms import AddUserForm, create_mediathequeForm
from mediatheque.models import Mediatheque


# Create your views here.
def index(request):
    return render(request, 'administration/index.html')


# Fonction pour afficher les utilisateurs de la base de données
def print_users(request):
    # On récupère tous les utilisateurs de la base de données ainsi que leurs informations
    users = User.objects.all()
    # On les affiche dans la page users.html
    return render(request, 'administration/users.html', {'users': users})

# Fonction qui permet de supprimer un ou plusieurs utilisateurs
def delete_users(request):
    if request.method == 'POST':
        # On récupère les id des utilisateurs à supprimer dans les checkbox cochées
        users = request.POST.getlist('users')
        for user in users:
            User.objects.get(id=user).delete()
        return redirect('print_users')

# Fonction qui permet de modifier les informations d'un utilisateur
def edit_user(request, id):
    if request.method == 'POST':
        # On récupère l'utilisateur dont l'id est passé en paramètre
        # user_info = User.objects.get(id=id)
        user_info = get_object_or_404(User, id=id)
        # On vérifie si le nom d'utilisateur est déjà utilisé
        if User.objects.filter(username=request.POST['username']).exists():
            if user_info.username != request.POST['username']:
                # On affiche un message d'erreur
                messages.error(request, "Ce nom d'utilisateur est déjà utilisé")
                # On redirige vers la page d'édition de l'utilisateur
                return redirect('edit_user', id=id)
            else:
                # On modifie les informations de l'utilisateur
                user_info.username = request.POST['username']
                user_info.email = request.POST['email']
                user_info.first_name = request.POST['first_name']
                user_info.last_name = request.POST['last_name']
                if 'is_active' in request.POST:
                    user_info.is_active = True
                else:
                    user_info.is_active = False
                if 'is_staff' in request.POST:
                    user_info.is_staff = True
                else:
                    user_info.is_staff = False
                if 'is_superuser' in request.POST:
                    user_info.is_superuser = True
                else:
                    user_info.is_superuser = False
                # On sauvegarde les modifications
                user_info.save()
                # On redirige vers la page des utilisateurs
                return redirect('print_users')
    # On récupère l'utilisateur dont l'id est passé en paramètre
    user_info = User.objects.get(id=id)
    context = {'user_info': user_info}
    # On affiche le formulaire d'édition de l'utilisateur
    return render(request, 'administration/edit_user.html', context)



# Fonction qui permet de créer un utilisateur
def create_user(request):
    form = AddUserForm(request.POST or None)
    # On vérifie si le formulaire est valide
    if form.is_valid():
        # On sauvegarde les informations de l'utilisateur
        form.save()
        return redirect('print_users')
    return render(request, 'administration/create_user.html', {'form': form})

# Fonction qui permet de créer une mediatheque
def create_mediatheque(request):
    if request.method == 'POST':
        form = create_mediathequeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_admin')
    else:
        form = create_mediathequeForm()
    return render(request, 'administration/create_mediatheque.html', {'form': form})

# Fonction qui récupère la liste des médiathèques
def get_mediatheques(request):
    mediatheques = Mediatheque.objects.all()
    return render(request, 'administration/list_mediatheque.html', {'mediatheques': mediatheques})

# Fonction qui permet d'afficher les informations des médithèques
def mediatheque_info(request, id):
    mediatheque = Mediatheque.objects.get(id=id)
    return render(request, 'administration/print_mediatheque.html', {'mediatheque': mediatheque})

# Fonction qui permet de modifier les informations d'une médiathèque
def edit_mediatheque(request, id):
    if request.method == 'POST':
        mediatheque = Mediatheque.objects.get(id=id)
        mediatheque.nom = request.POST['nom']
        mediatheque.adresse = request.POST['adresse']
        mediatheque.telephone = request.POST['telephone']
        mediatheque.save()
        return redirect('get_mediatheques')
    mediatheque = Mediatheque.objects.get(id=id)
    return render(request, 'administration/edit_mediatheque.html', {'mediatheque': mediatheque})