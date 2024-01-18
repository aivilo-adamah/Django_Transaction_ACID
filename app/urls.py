
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CompteViewSet, UtilisateurViewSet, transationAtomic

router = DefaultRouter()
router.register('utilisateurs', UtilisateurViewSet, basename='utilisateur')
router.register('comptes', CompteViewSet, basename='compte')


#router.register('transactions', transactionViewSet, basename='transaction')

urlpatterns = [
    path('API/', include(router.urls)),
    # path('transfert/<int:expediteur_id>/<int:destinataire_id>/<int:montant>/', effectuer_transaction, name='transfert'),
    # path('envoyer-sms/<str:expediteur_numero>/<str:destinataire_numero>/<int:montant>/', envoyer_sms, name='envoyer-sms'),
    path('', transationAtomic, name='effectuer-transaction'),
    


]