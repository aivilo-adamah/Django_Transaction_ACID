from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Utilisateur)
admin.site.register(models.Compte)
admin.site.register(models.Transaction)
