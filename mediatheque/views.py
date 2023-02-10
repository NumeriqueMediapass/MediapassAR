from django.shortcuts import render, redirect

from mediatheque.forms import AnimationForm, AnimationUpdateForm
from mediatheque.models import Animation


# Create your views here.

def index(request):
    return render(request, 'mediatheque/index.html', {})

def print_atelier(request):
    # On regarde si l'utilisateur est un admin
    if request.user.is_superuser:
        # On récupère toutes les animations
        animations = Animation.objects.all()
        return render(request, 'mediatheque/atelier.html', {'animations': animations})
    # On regarde si l'utilisateur est un staff
    elif request.user.is_staff:
        # On récupère les animations de la médiathèque de l'utilisateur
        animations = Animation.objects.filter(mediatheque__user=request.user)
        return render(request, 'mediatheque/atelier.html', {'animations': animations})

def add_atelier(request):
    if request.method == 'POST':
        form = AnimationForm(request.POST, request.FILES)
        if form.is_valid():
            animation = form.save(commit=False)
            animation.users = request.user
            animation.save()
            return redirect('print_atelier')
    else:
        form = AnimationForm()
    return render(request, 'mediatheque/add_atelier.html', {'form': form})

def edit_atelier(request, id):
    animation = Animation.objects.get(id=id)
    if request.method == 'POST':
        form = AnimationUpdateForm(request.POST, request.FILES, instance=animation)
        if form.is_valid():
            form.save()
            return redirect('print_atelier')
    else:
        form = AnimationUpdateForm(instance=animation)
    return render(request, 'mediatheque/edit_atelier.html', {'form': form})