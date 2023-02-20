from django import forms
from django.contrib.auth.admin import User
from django.contrib.auth.forms import PasswordChangeForm

from mediatheque.models import Reservation


# Class pour modifier le mot de passe d'un utilisateur
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


#Class pour modifier les informations d'un utilisateur
class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


# Class qui permet d'inscrire un utilisateur à une animation

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('user', 'animation')

# Class pour générer un calendrier
class CalendarWidget(forms.DateInput):
    template_name = 'widgets/calendar.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'form-control'
        return context