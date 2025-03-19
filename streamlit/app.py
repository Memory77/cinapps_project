import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# URL des API
URL_API_CRUD = os.getenv('URL_API_CRUD')  # API CRUD
URL_API_PRED = os.getenv('URL_API')  # API de prédiction

# 📌 Stocker le token JWT dans Streamlit
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# 📌 Fonction pour récupérer le token JWT
def get_access_token(username, password):
    data = {"username": username, "password": password}
    try:
        response = requests.post(f"{URL_API_CRUD}/auth/token", data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            st.error("🔴 Identifiants incorrects !")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Erreur de connexion à l'API : {str(e)}")
        return None

# 📌 Interface Streamlit : Connexion utilisateur
st.sidebar.title("🔐 Connexion")
username = st.sidebar.text_input("👤 Nom d'utilisateur")
password = st.sidebar.text_input("🔑 Mot de passe", type="password")
login_button = st.sidebar.button("Se connecter")

if login_button:
    token = get_access_token(username, password)
    if token:
        st.session_state["access_token"] = token
        st.sidebar.success("✅ Connexion réussie !")

# 📌 Fonction pour récupérer les films via l’API CRUD
def get_films_from_api():
    if not st.session_state["access_token"]:
        st.error("⚠️ Veuillez vous connecter pour accéder aux films.")
        return pd.DataFrame()

    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}

    try:
        response = requests.get(f"{URL_API_CRUD}/films/", headers=headers)
        if response.status_code == 200:
            films = response.json()
            return pd.DataFrame(films)
        else:
            st.error(f"⚠️ Erreur API CRUD : {response.status_code}")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Erreur de requête API CRUD : {str(e)}")
        return pd.DataFrame()

# 📌 Fonction pour nettoyer et vérifier les valeurs
def safe_value(value, default):
    if value is None or pd.isna(value):
        return default
    try:
        return int(value) if isinstance(default, int) else value
    except ValueError:
        return default

# 📌 Fonction pour faire les prédictions via l'API de prédiction
def get_predictions(film):
    headers = {'Content-Type': 'application/json'}
    
    # Vérification et conversion des valeurs
    data = {
        'budget': safe_value(film.get('budget'), 25000000),
        'duree': safe_value(film.get('duree'), 107),
        'genre': safe_value(film.get('genre'), 'missing'),
        'pays': safe_value(film.get('pays'), 'missing'),
        'salles_premiere_semaine': safe_value(film.get('salles'), 100),
        'scoring_acteurs_realisateurs': 0,
        'coeff_studio': 0,
        'year': safe_value(film.get('date_sortie', 2024), 2024)  # Vérifier si c'est un nombre
    }

    #print("📤 Données envoyées à l'API de prédiction :", data)  # Debug

    try:
        response = requests.post(URL_API_PRED, json=data, headers=headers)
        if response.status_code == 200:
            prediction = response.json()
            return safe_value(prediction.get('prediction'), 0)
        else:
            print(f"⚠️ Erreur API de prédiction : {response.status_code} - {response.text}")
            return f"Erreur API: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erreur de requête: {str(e)}"

# 📌 Interface principale
st.title("🎬 Prédiction d'entrées pour les films")

# 🔥 Vérifier si l'utilisateur est connecté avant de récupérer les films
if st.session_state["access_token"]:
    films = get_films_from_api()

    if films.empty:
        st.warning("⚠️ Aucun film trouvé dans la base de données.")
    else:
        # Appliquer la prédiction sur chaque film
        films["prediction_entrees"] = films.apply(get_predictions, axis=1)

        # Trier les films par nombre d'entrées décroissant
        films_sorted = films.sort_values(by="prediction_entrees", ascending=False)

        # 🔥 Affichage des films avec prédictions
        st.write("🎬 **Top Films avec prédictions**")
        st.dataframe(films_sorted)

        # 🔥 Graphique des prédictions
        st.bar_chart(films_sorted.set_index("titre")["prediction_entrees"])
else:
    st.warning("⚠️ Veuillez vous connecter pour afficher les films et les prédictions.")
