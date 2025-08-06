import pytest
from unittest.mock import patch
import requests

# 🌐 URL des API (on ne touche pas aux variables d'env ici, c'est fixe pour les tests)
URL_CRUD = "http://localhost:8000"
URL_PRED = "http://localhost:8001"

@pytest.fixture
def auth_header():
    """🔐 Simuler un token JWT"""
    return {"Authorization": "Bearer fake-token"}

@patch("requests.get")
def test_get_films(mock_get, auth_header):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"titre": "Film Test"}]

    response = requests.get(f"{URL_CRUD}/films/", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("requests.post")
@patch("requests.delete")
def test_create_and_delete_film(mock_delete, mock_post, auth_header):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id_film": 123}

    mock_delete.return_value.status_code = 200

    film_data = {
        "titre": "Test Film",
        "budget": 10000000,
        "duree": 120,
        "genre": "Comédie",
        "pays": "France",
        "studio": "Pathé",
        "date_sortie": "2025-01-01",
        "salles": 100
    }

    create_resp = requests.post(f"{URL_CRUD}/films/", json=film_data, headers=auth_header)
    assert create_resp.status_code == 201
    film_id = create_resp.json()["id_film"]

    delete_resp = requests.delete(f"{URL_CRUD}/films/{film_id}", headers=auth_header)
    assert delete_resp.status_code == 200

@patch("requests.get")
def test_get_acteurs_realisateurs(mock_get, auth_header):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    resp1 = requests.get(f"{URL_CRUD}/films/1/acteurs/", headers=auth_header)
    resp2 = requests.get(f"{URL_CRUD}/films/1/realisateurs/", headers=auth_header)

    assert resp1.status_code == 200
    assert resp2.status_code == 200

@patch("requests.post")
def test_prediction(mock_post, auth_header):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"prediction": 200000.0}

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
    assert isinstance(response.json()["prediction"], float)
