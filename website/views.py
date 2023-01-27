from django.shortcuts import render

# Create your views here.

def acceuil(request):
    return render(request, 'website/acceuil.html')