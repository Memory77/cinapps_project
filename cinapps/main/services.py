import requests
import os

API_URL = os.getenv('API_CRUD_URL')

def get_token_from_request(request):
    token = request.session.get("api_token")
    if not token:
        raise Exception("Token API manquant dans la session utilisateur.")
    return token

def get_films(request):
    token = get_token_from_request(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/films/", headers=headers)
    response.raise_for_status()
    return response.json()

def get_acteurs(request, film_id):
    token = get_token_from_request(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/films/{film_id}/acteurs/", headers=headers)
    if response.status_code == 404:
        return []
    response.raise_for_status()
    return response.json()

def get_realisateurs(request, film_id):
    token = get_token_from_request(request)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/films/{film_id}/realisateurs/", headers=headers)
    if response.status_code == 404:
        return []
    response.raise_for_status()
    return response.json()
