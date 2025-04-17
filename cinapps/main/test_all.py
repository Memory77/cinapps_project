import os
import requests
from dotenv import load_dotenv

load_dotenv()

crud_url = os.getenv("API_CRUD_URL")
username = os.getenv("API_CRUD_USERNAME")
password = os.getenv("API_CRUD_PASSWORD")
pred_url = os.getenv("URL_API")

# Obtenir le token
resp = requests.post(f"{crud_url}/auth/token", data={
    "username": username,
    "password": password
})
print("\n🎫 Token :")
print(resp.status_code, resp.text)

if resp.status_code != 200:
    exit()

token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Appeler les films
print("\n🎬 Films disponibles :")
films_resp = requests.get(f"{crud_url}/films/", headers=headers)
print(films_resp.status_code)
print(films_resp.json()[:2])  # affiche juste 2 films pour exemple

# Tester prédiction
print("\n🔮 Prédiction test :")
data = {
    "budget": 20000000,
    "duree": 120,
    "genre": "Action",
    "pays": "USA",
    "salles_premiere_semaine": 450,
    "scoring_acteurs_realisateurs": 0.7,
    "coeff_studio": 3,
    "year": 2024
}
pred_resp = requests.post(pred_url, headers=headers, json=data)
print(pred_resp.status_code, pred_resp.text)
