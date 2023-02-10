from django import forms

from mediatheque.models import Animation


# Formulaire qui permet la création d'une animation
class AnimationForm(forms.ModelForm):
    class Meta:
        model = Animation
        fields = ('name', 'description', 'date', 'hour', 'hour_end',  'age', 'age_end', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour': forms.TimeInput(attrs={'type': 'time'}),
            'hour_end': forms.TimeInput(attrs={'type': 'time'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        date = cleaned_data.get('date')
        hour = cleaned_data.get('hour')
        hour_end = cleaned_data.get('hour_end')
        age = cleaned_data.get('age')
        age_end = cleaned_data.get('age_end')
        image = cleaned_data.get('image')

        if not name:
            raise forms.ValidationError("Vous devez saisir un nom")
        if not description:
            raise forms.ValidationError("Vous devez saisir une description")
        if not date:
            raise forms.ValidationError("Vous devez saisir une date")
        if not hour:
            raise forms.ValidationError("Vous devez saisir une heure de début")
        if not hour_end:
            raise forms.ValidationError("Vous devez saisir une heure de fin")
        if not age:
            raise forms.ValidationError("Vous devez saisir un âge minimum")
        if not age_end:
            raise forms.ValidationError("Vous devez saisir un âge maximum")
        if not image:
            raise forms.ValidationError("Vous devez saisir une image")

        if age > age_end:
            raise forms.ValidationError("L'âge minimum doit être inférieur à l'âge maximum")

        if hour > hour_end:
            raise forms.ValidationError("L'heure de début doit être inférieure à l'heure de fin")

        return cleaned_data

# Class pour la modification d'une animation
class AnimationUpdateForm(forms.ModelForm):
    class Meta:
        model = Animation
        fields = ('name', 'description', 'date', 'hour', 'hour_end',  'age', 'age_end', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'datetime'}),
            'hour': forms.TimeInput(attrs={'type': 'time'}),
            'hour_end': forms.TimeInput(attrs={'type': 'time'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        date = cleaned_data.get('date')
        hour = cleaned_data.get('hour')
        hour_end = cleaned_data.get('hour_end')
        age = cleaned_data.get('age')
        age_end = cleaned_data.get('age_end')
        image = cleaned_data.get('image')