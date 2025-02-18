from django.contrib.auth.models import AbstractUser
from django.db import models

# Ceci est un modèle utilisateur personnalisé qui hérite actuellement de AbstractUser.
# Il est prêt à être étendu avec des champs et méthodes supplémentaires si besoin.(comme birth_date ici)
# Si aucun champ supplémentaire n'est requis au-delà du modèle par défaut de Django,
# cette classe peut rester vide et AbstractUser sera utilisé comme tel. 
class User(AbstractUser):
    birth_date = models.DateField(auto_now=False, null=True)
    

#stocker les informations de l'api en bdd
class PredApi(models.Model):
    pass

class PredictionFilm(models.Model):
    titre = models.CharField(max_length=255)
    prediction_entrees = models.IntegerField()

    def __str__(self):
        return self.titre

from django.db import models

class Film(models.Model):
    titre = models.CharField(max_length=255)
    duree = models.IntegerField(null=True, blank=True)
    salles = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
    date_sortie = models.DateField(null=True, blank=True)
    pays = models.CharField(max_length=255, null=True, blank=True)
    studio = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    budget = models.BigIntegerField(null=True, blank=True)
    entrees = models.BigIntegerField(null=True, blank=True)
    anecdotes = models.TextField(null=True, blank=True)
    film_url = models.CharField(max_length=255, null=True, blank=True)
    is_pred = models.BooleanField(default=False)  # Ajout de is_pred

    def __str__(self):
        return self.titre

