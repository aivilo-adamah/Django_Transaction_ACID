from django.shortcuts import render
from .serializers import CompteSerializer, TransactionSerializer, UtilisateurSerializer
from .forms import TransactionForm
from .models import Compte, Transaction, Utilisateur
from django.shortcuts import render, HttpResponseRedirect
from rest_framework import viewsets
from django.db import  transaction

from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioException
from django.contrib import messages


from django.core.mail import send_mail


# Create your views here.

def envoi_sms(expediteur_nom, destinataire_nom, montant):
    # identifiants Twilio
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_phone_number = settings.TWILIO_PHONE_NUMBER

    try:
        # Initialisation du client Twilio
        client = Client(account_sid, auth_token)

        # Récupération l'objet Utilisateur correspondant à l'expéditeur
        expediteur = Utilisateur.objects.get(nom=expediteur_nom)

        # Message à l'expéditeur
        expediteur_message = f"Vous avez envoyé {montant} à {destinataire_nom}"
        client.messages.create(
            body=expediteur_message,
            from_=from_phone_number,
            to=expediteur.numero_telephone
        )

        # Récupération de  l'objet Utilisateur correspondant au destinataire
        destinataire = Utilisateur.objects.get(nom=destinataire_nom)

        # Message au destinataire
        destinataire_message = f"Vous avez reçu {montant} de {expediteur_nom}"
        client.messages.create(
            body=destinataire_message,
            from_=from_phone_number,
            to=destinataire.numero_telephone
        )

        print("SMS envoyés avec succès!")

    except Utilisateur.DoesNotExist:
        print(f"Erreur: Utilisateur non trouvé. Vérifiez le nom d'expéditeur et de destinataire.")

    except TwilioException as e:
        # En cas d'erreur Twilio, afficher un message explicite
        print(f"Erreur Twilio: {e}")

    except Exception as e:
        # En cas d'autres erreurs, afficher un message explicite
        print(f"Erreur lors de l'envoi de SMS: {e}")    # identifiants Twilio
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_phone_number = settings.TWILIO_PHONE_NUMBER

   


   


def transationAtomic(request):
    form = TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(data=request.POST)

        if form.is_valid():
            expediteur_nom = form.cleaned_data.get('expediteur_nom')
            destinataire_nom = form.cleaned_data.get('destinataire_nom')
            montant = form.cleaned_data.get('montant')

            # Vérification que le montant est positif

            if montant <= 0:
                form.add_error('montant', 'Le montant doit être positif.')
                messages.error(request, "Erreur: Montant invalide")
                return render(request, 'index.html', {'form': form})


            with transaction.atomic():
                try:
                    expediteur = Utilisateur.objects.get(nom=expediteur_nom)
                    destinataire = Utilisateur.objects.get(nom=destinataire_nom)

                    print(f"Expediteur trouvé: {expediteur}")
                    print(f"Destinataire trouvé: {destinataire}")

                    # Vérifions que le montant est bien disponible sur le compte de l'expéditeur
                    if expediteur.compte.montant < montant:
                        form.add_error('montant', 'Montant non disponible sur le compte.')
                        messages.error(request, "Erreur: Montant non disponible")
                        return render(request, 'index.html', {'form': form})
                    

                    expediteur.compte.montant -= montant
                    expediteur.compte.save()

                    destinataire.compte.montant += montant
                    destinataire.compte.save()

                    # Envoi des SMS
                    envoi_sms(expediteur_nom, destinataire_nom, montant)

                    # Enregistrement de la transaction
                    transaction_obj = Transaction(
                        expediteur_nom=expediteur_nom,
                        destinataire_nom=destinataire_nom,
                        montant=montant
                    )
                    transaction_obj.save()

                    messages.success(request, "Transaction effectuée avec succès!")

                    print("Redirection à '/'.")
                    return HttpResponseRedirect('/')

                except Utilisateur.DoesNotExist:
                    print(f"L'utilisateur {expediteur_nom} ou {destinataire_nom} n'existe pas.")
                    form.add_error(None, f"L'utilisateur {expediteur_nom} ou {destinataire_nom} n'existe pas.")
                    messages.error(request, "Erreur: Utilisateur non trouvé")

    return render(request, 'index.html', {'form': form})




class UtilisateurViewSet(viewsets.ModelViewSet):
    serializer_class = UtilisateurSerializer
    queryset =Utilisateur.objects.all()




class CompteViewSet(viewsets.ModelViewSet):
    serializer_class = CompteSerializer
    queryset =Compte.objects.all()



class transactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset =Transaction.objects.all()


