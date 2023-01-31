from django.shortcuts import redirect, render

from website.forms import UserForm

# Create your views here.

def acceuil(request):
    return render(request, 'website/acceuil.html')

def monCompte(request):
    form = UserForm(request.POST or None)
    return render(request, 'website/monCompte.html',{'form': form})