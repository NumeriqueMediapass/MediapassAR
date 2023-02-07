from django import forms
from django.contrib.auth.models import User

#Formulaire pour modifier les informations d'un utilisateur
class EditProfileForm(forms.ModelForm):
     class Meta:
         model = User
         fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
         labels = {
             'username': 'Nom d\'utilisateur',
             'email': 'Adresse email',
             'first_name': 'Prénom',
             'last_name': 'Nom',
             'is_active': 'Active',
             'is_staff': 'Staff',
             'is_superuser': 'Superuser',
         }
         widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control'}),
             'email': forms.TextInput(attrs={'class': 'form-control'}),
             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
             'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
             'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
         }

     def clean_username(self):
         username = self.cleaned_data['username']
         if User.objects.filter(username=username).exists():
             raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé")
         return username
