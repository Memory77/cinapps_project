import os
import pytest
import requests
from dotenv import load_dotenv
from random import randint

load_dotenv()

# 📦 Récupération des variables d’environnement
URL_CRUD = os.getenv("URL_API_CRUD", "http://localhost:8000")
URL_PRED = os.getenv("URL_API", "http://localhost:8001")
USERNAME = os.getenv("API_CRUD_USERNAME", "deborah")
PASSWORD = os.getenv("API_CRUD_PASSWORD", "deborahdeborah")


@pytest.fixture(scope="module")
def token():
    """🔐 Obtenir un JWT depuis l'API CRUD"""
    response = requests.post(
        f"{URL_CRUD}/auth/token",
        data={"username": USERNAME, "password": PASSWORD}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


### 🌟 TEST CRUD API ###
def test_get_films(auth_header):
    response = requests.get(f"{URL_CRUD}/films/", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_delete_film(auth_header):
    film_data = {
        "titre": f"Test Film {randint(1, 10000)}",
        "budget": 10000000,
        "duree": 120,
        "genre": "Comédie",
        "pays": "France",
        "studio": "Pathé",
        "date_sortie": "2025-01-01",
        "salles": 100
    }
    # 🔼 Création
    create_resp = requests.post(f"{URL_CRUD}/films/", json=film_data, headers=auth_header)
    assert create_resp.status_code == 201
    film_id = create_resp.json()["id_film"]

    # ❌ Suppression
    delete_resp = requests.delete(f"{URL_CRUD}/films/{film_id}", headers=auth_header)
    assert delete_resp.status_code == 200


def test_get_acteurs_realisateurs(auth_header):
    response = requests.get(f"{URL_CRUD}/films/1/acteurs/", headers=auth_header)
    assert response.status_code in [200, 404]  # si pas de film 1, normal

    response = requests.get(f"{URL_CRUD}/films/1/realisateurs/", headers=auth_header)
    assert response.status_code in [200, 404]


#TEST API DE PRÉDICTION ###
def test_prediction(auth_header):
    payload = {
        "budget": 25000000,
        "duree": 120,
        "genre": "Action",
        "pays": "USA",
        "salles_premiere_semaine": 450,
        "scoring_acteurs_realisateurs": 0.78,
        "coeff_studio": 3,
        "year": 2024
    }

    response = requests.post(f"{URL_PRED}/prediction/", json=payload, headers=auth_header)
    assert response.status_code == 200
    body = response.json()
    assert "prediction" in body
    assert isinstance(body["prediction"], float)
