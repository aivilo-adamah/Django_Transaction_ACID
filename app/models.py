from django.db import models

# Create your models here.

import uuid
from django.db import models

# Create your models here.

class Utilisateur (models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50)
    prenoms = models.CharField(max_length=50)
    numero_telephone = models.CharField(max_length=15) 
    email = models.EmailField(default = 'adamaholivia444@gmail.com')

   

class Compte(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numeroCpt = models.CharField(max_length=10)
    montant = models.IntegerField()
    proprietaire = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='compte')

    def __str__(self):
        return f"{self.numeroCpt} {self.proprietaire.nom}"


    


class Transaction(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expediteur_nom = models.CharField(max_length=50)
    destinataire_nom = models.CharField(max_length=50)
    montant = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction de {self.expediteur_nom} vers {self.destinataire_nom}"

    


