from django import forms
from django.contrib.auth.models import User

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
        email = self.cleaned_data.get('email')