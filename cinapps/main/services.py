import os
import requests

def get_api_token():
    url = f"{os.getenv('API_CRUD_URL')}/auth/token"
    username = os.getenv("API_CRUD_USERNAME")
    password = os.getenv("API_CRUD_PASSWORD")

    try:
        response = requests.post(url, data={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Erreur token: {response.status_code} - {response.text}")
            return None

    except requests.RequestException as e:
        print(f"❌ Exception lors de l'obtention du token: {e}")
        return None


def get_films_from_api():
    token = get_api_token()
    if not token:
        return []

    url = f"{os.getenv('API_CRUD_URL')}/films/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erreur films: {response.status_code} - {response.text}")
            return []
    except requests.RequestException as e:
        print(f"❌ Exception lors de la récupération des films: {e}")
        return []


def get_acteurs_by_film_api(film_id):
    token = get_api_token()
    if not token:
        return []

    url = f"{os.getenv('API_CRUD_URL')}/films/{film_id}/acteurs/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return [a['nom'] for a in data]
        else:
            print(f"❌ Erreur acteurs pour film {film_id}: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Exception acteurs: {e}")
        return []


def get_realisateurs_by_film_api(film_id):
    token = get_api_token()
    if not token:
        return []

    url = f"{os.getenv('API_CRUD_URL')}/films/{film_id}/realisateurs/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return [r['nom'] for r in data]
        else:
            print(f"❌ Erreur réalisateurs pour film {film_id}: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Exception réalisateurs: {e}")
        return []
