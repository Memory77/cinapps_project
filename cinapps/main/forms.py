from django import forms 
from .models import PredApi


class AvisForm(forms.Form):
    note = forms.IntegerField(
        min_value=1, max_value=5, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Note entre 1 et 5'})
    )
    commentaire = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ton avis'}),
        required=False
    )
    id_film = forms.IntegerField(widget=forms.HiddenInput())
