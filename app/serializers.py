from rest_framework import serializers
from .models import Compte, Transaction, Utilisateur





class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__' 



class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = '__all__' 




class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__' 
