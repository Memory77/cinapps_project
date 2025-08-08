from django.test import SimpleTestCase, TestCase, Client
from unittest.mock import patch
import pandas as pd
from main.functions import scoring_casting
from main.views import get_predictions
from main.services import get_films_from_api
from django.contrib.auth.models import User


### 1. Test d’une fonction pure (pas de DB, pas de mock) ###
class FunctionTest(SimpleTestCase):
    def test_scoring_casting_basic(self):
        film = {'acteurs': ['John'], 'realisateurs': ['Jane']}
        actors_df = pd.DataFrame({
            'name': ['John', 'Jane'],
            'coef_personne': [2.0, 3.0]
        })
        result = scoring_casting(film, actors_df)
        self.assertEqual(result, 5.0)


### 2. Test API CRUD (mocké) ###
class APICRUDTest(SimpleTestCase):

    @patch("main.services.requests.get")
    @patch("main.services.get_api_token")
    def test_get_films_from_api_returns_data(self, mock_token, mock_get):
        mock_token.return_value = "fake-token"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"titre": "Film A"}]

        films = get_films_from_api()
        self.assertEqual(len(films), 1)
        self.assertEqual(films[0]['titre'], "Film A")


### 3. Test API prédiction (mocké) ###
class PredictionTest(SimpleTestCase):

    @patch("main.views.PredictionFilm.objects.update_or_create")  # pour éviter la DB
    @patch("main.views.requests.post")
    @patch("main.views.get_api_token")
    def test_get_predictions_adds_fields(self, mock_token, mock_post, mock_update):
        mock_token.return_value = "token"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"prediction": 200000.0}

        films = [{
            'titre': 'Fake Movie',
            'budget': 10000000,
            'duree': 90,
            'genre': 'Action',
            'pays': 'France',
            'salles': 100,
            'studio': 'Universal',
            'date_sortie': '2025-01-01',
            'scoring_acteurs_realisateurs': 4,
            'coeff_studio': 3
        }]

        results = get_predictions(films)
        self.assertEqual(results[0]['prediction_entrees'], 200000)
        self.assertIn('estimation_recette_hebdo', results[0])


class ViewTest(TestCase):
    @patch("main.views.get_predictions")
    @patch("main.views.get_realisateurs_by_film_api")
    @patch("main.views.get_acteurs_by_film_api")
    @patch("main.views.get_films_from_api")
    def test_home_page_works(self, mock_films, mock_acteurs, mock_realisateurs, mock_predict):
        user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        
        mock_films.return_value = [{
            'id_film': 1,
            'titre': 'Test Film',
            'budget': 10000000,
            'duree': 100,
            'genre': 'Comédie',
            'pays': 'France',
            'salles': 100,
            'studio': 'Pathé',
            'date_sortie': '2025-01-01'
        }]
        mock_acteurs.return_value = ['Acteur A']
        mock_realisateurs.return_value = ['Réalisateur A']
        mock_predict.side_effect = lambda films: [{
            **films[0],
            'scoring_acteurs_realisateurs': 5,
            'coeff_studio': 2,
            'prediction_entrees': 123456,
            'estimation_recette_hebdo': 600000
        }]

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home_page.html")
        self.assertIn("films", response.context)
        self.assertEqual(response.context["films"][0]["prediction_entrees"], 123456)

# ### 4. Test Vue home_page (mocké à fond) ###
# class ViewTest(TestCase):

#     @patch("main.views.get_predictions")
#     @patch("main.views.get_realisateurs_by_film_api")
#     @patch("main.views.get_acteurs_by_film_api")
#     @patch("main.views.get_films_from_api")
#     def test_home_page_works(self, mock_films, mock_acteurs, mock_realisateurs, mock_predict):
#         mock_films.return_value = [{
#             'id_film': 1,
#             'titre': 'Test Film',
#             'budget': 10000000,
#             'duree': 100,
#             'genre': 'Comédie',
#             'pays': 'France',
#             'salles': 100,
#             'studio': 'Pathé',
#             'date_sortie': '2025-01-01'
#         }]
#         mock_acteurs.return_value = ['Acteur A']
#         mock_realisateurs.return_value = ['Réalisateur A']
#         mock_predict.side_effect = lambda films: [{
#             **films[0],
#             'scoring_acteurs_realisateurs': 5,
#             'coeff_studio': 2,
#             'prediction_entrees': 123456,
#             'estimation_recette_hebdo': 600000
#         }]

#         client = Client()
#         response = client.get("/")
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "main/home_page.html")
#         self.assertIn("films", response.context)
#         self.assertEqual(response.context["films"][0]["prediction_entrees"], 123456)


# Petit exemple ultra simple :

# Tu as ce test dans tests.py :

# def test_prediction_is_calculated_correctly(self):
#     self.assertEqual(prediction_result, 200000)

# Et dans ton vrai code (views.py, services.py, etc.) t’as :

# film['prediction_entrees'] = int(float(prediction['prediction']))

# Maintenant, imagine que tu changes accidentellement ce code comme ça :

# film['prediction_entrees'] = prediction['prediction'] / 100

# ➡️ BOOM 💥 Ton test va échouer !
# Parce qu’il attendait 200000, et maintenant le code renvoie 2000.
# Donc GitHub va détecter un échec, même si tu n’as pas touché au test lui-même