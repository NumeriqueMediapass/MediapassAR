from django import forms
from django.contrib.auth.models import User
from mediatheque.models import Mediatheque

# Formulaire pour ajouter un utilisateur
class AddUserForm(forms.ModelForm):
     class Meta:
         model = User
         fields = ('username', 'email', 'first_name', 'last_name',  'password','is_active', 'is_staff', 'is_superuser')
         labels = {
             'username': 'Nom d\'utilisateur',
             'email': 'Adresse email',
             'first_name': 'Prénom',
             'last_name': 'Nom',
             'password': 'Mot de passe',
             'is_active': 'Active',
             'is_staff': 'Staff',
             'is_superuser': 'Superuser',
         }
         widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control'}),
             'email': forms.TextInput(attrs={'class': 'form-control'}),
             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
             'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
             'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
         }

     def clean_username(self):
         username = self.cleaned_data['username']
         if User.objects.filter(username=username).exists():
             raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé")
         return username

class create_mediathequeForm(forms.ModelForm):
    class Meta:
        model = Mediatheque
        fields = ('name', 'address', 'phone', 'email','user')
        labels = {
            'name': 'Nom de la médiathèque',
            'address': 'Adresse',
            'phone': 'Téléphone',
            'email': 'Email',
            'user': 'Utilisateur',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

    # On regarde si le nom est déjà utilisé dans une autre médiathèque
    def clean_name(self):
        name = self.cleaned_data['name']
        if Mediatheque.objects.filter(name=name).exists():
            raise forms.ValidationError("Ce nom est déjà utilisé")
        return name

    # On regarder si l'utilisateur est déjà utilisé dans une autre médiathèque
    def clean_user(self):
        user = self.cleaned_data['user']
        if Mediatheque.objects.filter(user=user).exists():
            raise forms.ValidationError("Cet utilisateur est déjà utilisé")
        return user