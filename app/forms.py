
from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    expediteur_nom = forms.CharField(max_length=50)
    destinataire_nom = forms.CharField(max_length=50)
    montant = forms.IntegerField()

    class Meta:
        model = Transaction
        fields = ['expediteur_nom', 'destinataire_nom', 'montant']