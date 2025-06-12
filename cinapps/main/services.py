import os
import requests

#va récupérer automatiquement un token JWT au nom d'un compte générique 
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
    print(f"🔑 TOKEN UTILISÉ : {token}")  # Ajout debug

    if not token:
        print("❌ Aucun token récupéré")
        return []

    url = f"{os.getenv('API_CRUD_URL')}/films/"
    print(f"📡 Requête vers : {url}")  # Ajout debug

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"📦 Code retour : {response.status_code}")  # Ajout debug

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

def get_avis_by_film_api(film_id):
    token = get_api_token()
    if not token:
        return []

    url = f"{os.getenv('API_CRUD_URL')}/avis/film/{film_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erreur récupération avis pour film {film_id}: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Exception lors de get_avis_by_film_api : {e}")
        return []
        
def post_avis_to_api(id_film, username, note, commentaire):
    token = get_api_token()
    if not token:
        print("❌ Aucun token pour poster un avis")
        return False

    url = f"{os.getenv('API_CRUD_URL')}/avis/avis/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "id_film": id_film,
        "username": username,
        "note": note,
        "commentaire": commentaire
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("✅ Avis posté avec succès")
            return True
        else:
            print(f"❌ Erreur post avis: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"❌ Exception lors du post d'avis: {e}")
        return False
