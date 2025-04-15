from django.shortcuts import render
import os
import json
import pandas as pd
import requests
from datetime import datetime
from decimal import Decimal
from .models import PredictionFilm
from .functions import scoring_casting, get_studio_coefficient
from .services import get_films_from_api, get_acteurs_by_film_api, get_realisateurs_by_film_api


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


# Charger le CSV une seule fois
actors = pd.read_csv('main/acteurs_coef.csv')


def home_page(request):
    # 1. Récupérer les films depuis l’API CRUD
    films = get_films_from_api()

    for film in films:
        # 2. Ajouter acteurs et réalisateurs
        film['acteurs'] = get_acteurs_by_film_api(film['id_film'])
        film['realisateurs'] = get_realisateurs_by_film_api(film['id_film'])

        # 3. Calcul du scoring et du coefficient studio
        film['scoring_acteurs_realisateurs'] = scoring_casting(film, actors)
        film['coeff_studio'] = get_studio_coefficient(film['studio'])

    # 4. Lancer les prédictions
    films = get_predictions(films)

    # 5. Trier les films selon prédiction décroissante
    films_sorted = sorted(
        films,
        key=lambda x: int(x.get('prediction_entrees', 0)) if str(x.get('prediction_entrees', '0')).isdigit() else 0,
        reverse=True
    )

    # 6. Top 10 + Top 2 pour bénéfice
    top_ten_films = films_sorted[:10]
    top_two_films = films_sorted[:2]

    ch_affaires = sum(film['estimation_recette_hebdo'] for film in top_two_films)
    charge = 4900
    benefice = ch_affaires - charge

    tab_result = {
        'ch_affaires': ch_affaires,
        'charge': charge,
        'benefice': benefice
    }

    return render(request, "main/home_page.html", {
        "films": top_ten_films,
        "top_two": top_two_films,
        "tab_result": tab_result
    })


def get_predictions(films):
    url = os.getenv('URL_API')
    headers = {'Content-Type': 'application/json'}

    for film in films:
        # Conversion date_sortie pour extraire l’année
        try:
            year = datetime.strptime(film['date_sortie'], "%Y-%m-%d").year if film['date_sortie'] else None
        except Exception as e:
            print(f"❌ Erreur parsing date_sortie pour {film['titre']} : {e}")
            year = None

        data = {
            'budget': film['budget'] if film['budget'] is not None else 25000000,
            'duree': film['duree'] if film['duree'] is not None else 107,
            'genre': film['genre'] if film['genre'] is not None else 'missing',
            'pays': film['pays'] if film['pays'] is not None else 'missing',
            'salles_premiere_semaine': film['salles'] if film['salles'] is not None else None,
            'scoring_acteurs_realisateurs': film.get('scoring_acteurs_realisateurs', 0),
            'coeff_studio': film.get('coeff_studio', 0),
            'year': year
        }

        try:
            json_data = json.dumps(data, cls=DecimalEncoder)
            response = requests.post(url, data=json_data, headers=headers)

            if response.status_code == 200:
                prediction = response.json()
                film['prediction_entrees'] = int(prediction['prediction'])
                film['estimation_entrees_cinema'] = int(film['prediction_entrees'] / 2000)
                film['estimation_entrees_quot'] = int(film['estimation_entrees_cinema'] / 7)
                film['estimation_recette_hebdo'] = film['estimation_entrees_cinema'] * 10

                PredictionFilm.objects.update_or_create(
                    titre=film['titre'],
                    defaults={'prediction_entrees': film['prediction_entrees']}
                )
            else:
                film['prediction_entrees'] = f"Erreur {response.status_code}: {response.text}"

        except Exception as e:
            print(f"❌ Exception prédiction pour {film['titre']} : {e}")
            film['prediction_entrees'] = "Erreur"

    return films


def chiffre_page(request):
    return render(request, 'main/chiffre_page.html')


def archive_page(request):
    return render(request, "main/archive_page.html")



import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Converts Decimal to string
        return super().default(obj)
    
    
#Lorsque vous configurez une tâche périodique avec Celery, celle-ci est exécutée de manière autonome selon
# l'horaire défini, et non pas à chaque fois que la page est appelée. Cela signifie que la tâche pour récupérer
# les films et obtenir les prédictions se déclenchera automatiquement à l'heure prévue chaque semaine, 
#indépendamment des requêtes des utilisateurs sur votre site web.

#Pour clarifier le fonctionnement :

#Planification de la tâche : La tâche est configurée pour s'exécuter à un moment spécifique 
#(par exemple, tous les lundis à minuit). Cette planification est gérée par Celery Beat, 
#qui surveille l'heure et déclenche l'exécution de la tâche conformément à son calendrier.
#Exécution indépendante : Une fois déclenchée par Celery Beat, la tâche s'exécute de manière indépendante 
#du cycle de vie des requêtes HTTP de votre site web. Elle fonctionne en arrière-plan et n'affecte pas les
# performances ou le fonctionnement de vos vues Django, sauf si vous avez configuré quelque chose pour que les 
#vues interagissent avec les résultats de cette tâche.
#Non-liée aux requêtes des utilisateurs : Les utilisateurs qui accèdent à votre site ne déclenchent pas cette tâche. Ils verront simplement les résultats (par exemple, les films et les prédictions) qui ont été générés et sauvegardés lors de la dernière exécution de la tâche.


#