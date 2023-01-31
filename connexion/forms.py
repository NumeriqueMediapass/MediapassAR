from django import forms
from django.contrib.auth.models import User

#Class pour s'inscrire
class SignupForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def clean_email(self):
            email = self.cleaned_data['email']
            #On regarde si l'adresse mail est déjà exsitante dans la base de donnée
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Cette adresse mail est déjà utilisée")
            return email

#Class pour réinitialiser le mot de passe avec l'email et un token envoyé par mail
class ResetPasswordForm(forms.Form):
    token = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Token'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')