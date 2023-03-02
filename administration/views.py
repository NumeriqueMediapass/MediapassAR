from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from administration.forms import EditMediathequeForm, create_mediathequeForm
from mediatheque.models import Mediatheque


# Create your views here.
def index(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    # On récupère la liste des dernières connexions avec la date et l'heure
    log = User.objects.all().order_by('-last_login')
    return render(request, 'administration/index.html', {'log': log})


# Fonction pour afficher les utilisateurs de la base de données
def UsersViews(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    # On récupère tous les utilisateurs de la base de données ainsi que leurs informations
    users = User.objects.all()
    print(users)
    res = Mediatheque.objects.all().count()
    print(res)
    # On les affiche dans la page users.html
    return render(request, 'administration/users.html', {'users': users , 'res': res})

# Fonction qui permet de supprimer un ou plusieurs utilisateurs
def UserDeletion(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')

    if request.method == 'POST':
        # On récupère les id des utilisateurs à supprimer dans les checkbox cochées
        users = request.POST.getlist('users')
        for user in users:
            User.objects.get(id=user).delete()
        return redirect('UsersViews')

# Fonction qui permet de modifier les informations d'un utilisateur
def UsersEdit(request, idusers):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    if request.method == 'POST':
        # On récupère l'utilisateur dont l'id est passé en paramètre
        # user_info = User.objects.get(id=id)
        user_info = get_object_or_404(User, id=idusers)
        # On vérifie si le nom d'utilisateur est déjà utilisé
        if User.objects.filter(username=request.POST['username']).exists():
            if user_info.username != request.POST['username']:
                # On affiche un message d'erreur
                messages.error(request, "Ce nom d'utilisateur est déjà utilisé")
                # On redirige vers la page d'édition de l'utilisateur
                return redirect('UsersEdit', id=idusers)
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
                return redirect('UsersViews')
    # On récupère l'utilisateur dont l'id est passé en paramètre
    user_info = User.objects.get(id=idusers)
    context = {'user_info': user_info}
    # On affiche le formulaire d'édition de l'utilisateur
    return render(request, 'administration/edit_user.html', context)



# Fonction qui permet de créer un utilisateur
def UsersCreation(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    form = UserCreationForm(request.POST or None)
    # On vérifie si le formulaire est valide
    if form.is_valid():
        # On sauvegarde les informations de l'utilisateur
        form.save()
        return redirect('UsersViews')
    return render(request, 'administration/create_user.html', {'form': form})

# Fonction qui permet de créer une mediatheque
def MediaLibraryCreations(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    if request.method == 'POST':
        form = create_mediathequeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MediaLibraryViews')
    else:
        form = create_mediathequeForm()
    return render(request, 'administration/create_mediatheque.html', {'form': form})

# Fonction qui récupère la liste des médiathèques
def MediaLibraryViews(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')
    mediatheques = Mediatheque.objects.all()
    return render(request, 'administration/list_mediatheque.html', {'mediatheques': mediatheques})


# Fonction qui permet de modifier les informations d'une médiathèque
def MediaLibraryEditing(request, idmedialibrary):
    # On vérifie si l'utilisateur est un superutilisateur ou un membre du personnel
    if not request.user.is_superuser and not request.user.is_staff:
        # On le redirige vers la page d'accueil
        return redirect('accueil')

    # On récupère l'objet Mediatheque correspondant à l'id donné, ou on renvoie une erreur 404 si l'id n'existe pas
    mediatheque = get_object_or_404(Mediatheque, id=idmedialibrary)

    if request.method == 'POST':
        form = EditMediathequeForm(request.POST, instance=mediatheque)
        if form.has_changed() and form.is_valid():
            form.save()
            messages.success(request, "La médiatheque a été modifiée")
            return redirect('MediaLibraryViews')
    else:
        form = EditMediathequeForm(instance=mediatheque)

    return render(request, 'administration/print_mediatheque.html', {'form': form})


# Fonction qui permet de supprimer une/des médiathèques
def MediaLibraryDelation(request):
    # On regarde si l'utilisateur est un utilisateur sans droits
    if not request.user.is_superuser or not request.user.is_staff:
        # On le renvoie vers la page d'accueil
        return redirect('acceuil')

    if request.method == 'POST':
        # On récupère les id des médiathèque à supprimer dans les checkbox cochées
        mediatheques = request.POST.getlist('mediatheques')
        for mediatheque in mediatheques:
            Mediatheque.objects.get(id=mediatheque).delete()
        return redirect('MediaLibraryViews')