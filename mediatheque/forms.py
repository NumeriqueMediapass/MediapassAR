from django import forms

from mediatheque.models import Animation


# Formulaire qui permet la création d'une animation
class AnimationForm(forms.ModelForm):
    class Meta:
        model = Animation
        fields = ('name', 'description', 'date', 'hour',  'age', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour': forms.TimeInput(attrs={'type': 'time'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }



    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        date = cleaned_data.get('date')
        hour = cleaned_data.get('hour')
        age = cleaned_data.get('age')
        image = cleaned_data.get('image')

        if not name:
            raise forms.ValidationError("Vous devez entrer un nom")
        if not description:
            raise forms.ValidationError("Vous devez entrer une description")
        if not date:
            raise forms.ValidationError("Vous devez entrer une date")
        if not hour:
            raise forms.ValidationError("Vous devez entrer une heure")
        if not age:
            raise forms.ValidationError("Vous devez entrer un age")
        if not image:
            raise forms.ValidationError("Vous devez entrer une image")

        return cleaned_data

# Class pour la modification d'une animation
class AnimationUpdateForm(forms.ModelForm):
    class Meta:
        model = Animation
        fields = ('name', 'description', 'date', 'hour',  'age', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour': forms.TimeInput(attrs={'type': 'time'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        date = cleaned_data.get('date')
        hour = cleaned_data.get('hour')
        age = cleaned_data.get('age')
        image = cleaned_data.get('image')

        return cleaned_data