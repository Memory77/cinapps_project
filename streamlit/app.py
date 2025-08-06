import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from monitoring.monitor_drift import generate_drift_report
from utils import scoring_casting, get_studio_coefficient

# 🌍 Charger les variables d'environnement
load_dotenv()
URL_API_CRUD = os.getenv('URL_API_CRUD')
URL_API_PRED = os.getenv('URL_API')
API_CRUD_USERNAME = os.getenv('API_CRUD_USERNAME')
API_CRUD_PASSWORD = os.getenv('API_CRUD_PASSWORD')

# 📦 Charger les coefficients des acteurs
actors_df = pd.read_csv("acteurs_coef.csv")

# 🔐 Authentification
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

if "access_token" not in st.session_state or not st.session_state["access_token"]:
    token = get_access_token(API_CRUD_USERNAME, API_CRUD_PASSWORD)
    if token:
        st.session_state["access_token"] = token
    else:
        st.stop()

# ⚙️ Utilitaires
def safe_value(value, default):
    if value is None or pd.isna(value):
        return default
    try:
        return int(value) if isinstance(default, int) else value
    except ValueError:
        return default

def get_films_from_api():
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    try:
        response = requests.get(f"{URL_API_CRUD}/films/", headers=headers)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"⚠️ Erreur API CRUD : {response.status_code}")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Erreur API CRUD : {str(e)}")
        return pd.DataFrame()

def get_predictions(film):
    token = st.session_state["access_token"]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    scoring = scoring_casting(film, actors_df)
    studio_coeff = get_studio_coefficient(film.get('studio', ''))

    try:
        year = pd.to_datetime(film.get('date_sortie')).year
    except:
        year = 2024

    data = {
        'budget': safe_value(film.get('budget'), 25000000),
        'duree': safe_value(film.get('duree'), 107),
        'genre': safe_value(film.get('genre'), 'missing'),
        'pays': safe_value(film.get('pays'), 'missing'),
        'salles_premiere_semaine': safe_value(film.get('salles'), 100),
        'scoring_acteurs_realisateurs': scoring,
        'coeff_studio': studio_coeff,
        'year': year
    }

    try:
        response = requests.post(URL_API_PRED, json=data, headers=headers)
        if response.status_code == 200:
            prediction = response.json()
            return safe_value(prediction.get('prediction'), 0)
        else:
            return 0
    except requests.exceptions.RequestException:
        return 0

# génération automatique de current.csv
def generate_current_csv_from_api():
    films = get_films_from_api()
    if films.empty:
        return False

    # Ajout des colonnes nécessaires
    films["scoring_acteurs_realisateurs"] = films.apply(lambda row: scoring_casting(row, actors_df), axis=1)
    films["coeff_studio"] = films["studio"].apply(lambda s: get_studio_coefficient(str(s)))

    # Colonnes à garder
    required_cols = [
        'acteurs', 'budget', 'compositeur', 'duree', 'entrees_premiere_semaine',
        'franchise', 'genre', 'pays', 'producteur', 'realisateur',
        'salles_premiere_semaine', 'studio', 'titre', 'scoring_acteurs_realisateurs',
        'coeff_studio', 'season', 'year'
    ]
    current = films[[col for col in required_cols if col in films.columns]]
    current.to_csv("monitoring/current.csv", index=False)
    return True

# ====================== INTERFACE STREAMLIT ======================

st.set_page_config(page_title="Cinapps", page_icon="🎬", layout="wide")
menu = st.sidebar.radio("🏷️ Navigation", ["🎬 Prédictions", "📊 Monitoring Drift"])

if menu == "🎬 Prédictions":
    st.title("🎬 Cinapps - Prédiction d'entrées cinéma")

    films = get_films_from_api()

    if films.empty:
        st.warning("⚠️ Aucun film trouvé.")
    else:
        with st.spinner("🔍 Prédictions en cours..."):
            films["prediction_entrees"] = films.apply(lambda row: get_predictions(row), axis=1)
            films_sorted = films.sort_values(by="prediction_entrees", ascending=False)

        st.subheader("🎯 Top 10 Prédictions")
        st.dataframe(films_sorted[["titre", "studio", "prediction_entrees"]].head(10), use_container_width=True)

        st.subheader("📊 Visualisation")
        st.bar_chart(films_sorted.set_index("titre")["prediction_entrees"].head(10))

elif menu == "📊 Monitoring Drift":
    st.title("📊 Monitoring du Drift de données (Evidently)")

    if st.button("✍️ Générer le rapport Evidently"):
        with st.spinner("🔄 Récupération des données de prod..."):
            if generate_current_csv_from_api():
                success = generate_drift_report()
                if success:
                    st.success("✅ Rapport généré !")
                    st.components.v1.html(open("monitoring/report/report.html", "r").read(), height=600, scrolling=True)
                else:
                    st.error("❌ Erreur lors de la génération du rapport.")
            else:
                st.warning("⚠️ Impossible de générer current.csv.")

    elif os.path.exists("monitoring/report/report.html"):
        st.components.v1.html(open("monitoring/report/report.html", "r").read(), height=600, scrolling=True)
    else:
        st.info("ℹ️ Aucun rapport Evidently trouvé.")
