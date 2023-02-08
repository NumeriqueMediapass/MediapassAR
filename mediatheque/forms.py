from django import forms

from mediatheque.models import Animation


# Formulaire qui permet la création d'une animation
class AnimationForm(forms.ModelForm):
    class Meta:
        model = Animation
        fields = ('name', 'description', 'date', 'hour',  'age', 'image','mediatheque')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'hour': forms.TimeInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'mediatheque': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AnimationForm, self).__init__(*args, **kwargs)
        self.fields['mediatheque'].empty_label = "Choisissez une médiathèque"

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get("heure_debut")
        heure_fin = cleaned_data.get("heure_fin")
        if heure_debut > heure_fin:
            raise forms.ValidationError("L'heure de début doit être inférieure à l'heure de fin")
        return cleaned_data
