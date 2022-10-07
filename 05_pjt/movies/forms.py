from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    score = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                'step': 0.5,
                'min': 0,
                'max': 5,
            }
        )
    )
    release_date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={
                'type':'date',
            }
        )
    )
    class Meta:
        model = Movie
        fields = ('__all__')