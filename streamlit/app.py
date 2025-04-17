import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# 🌍 Charger les variables d'environnement
load_dotenv()

URL_API_CRUD = os.getenv('URL_API_CRUD')
URL_API_PRED = os.getenv('URL_API')

# 📦 Charger les coefficients des acteurs
actors_df = pd.read_csv("acteurs_coef.csv")

# 🧠 Initialiser le token
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# 🔐 Fonction pour obtenir le token JWT
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

# 📥 Connexion
st.sidebar.title("🔐 Connexion")
username = st.sidebar.text_input("👤 Nom d'utilisateur")
password = st.sidebar.text_input("🔑 Mot de passe", type="password")
login_button = st.sidebar.button("Se connecter")

if login_button:
    token = get_access_token(username, password)
    if token:
        st.session_state["access_token"] = token
        st.sidebar.success("✅ Connexion réussie !")

# 📊 Coefficient studio
def get_studio_coefficient(studio):
    if studio in ('Walt Disney Pictures','Warner Bros.','Paramount','Sony Pictures','Universal','20th Century Fox','Lionsgate','Columbia'):
        return 3
    elif studio in ('Pathé','Studiocanal','Gaumont','UGC Distribution','SND','Le Pacte','Metropolitan','EuropaCorp','GBVI','Wild Bunch','UFD','ARP Selection','Ad vitam','Haut et Court','Films du Losange','Rezo Films','TFM Distribution'):
        return 2
    elif studio in ('Gébéka','Memento Films','KMBO','Océan Films','AMLF','MK2 Diffusion','Gaumont Sony','Apollo Films','Sophie Dulac','Eurozoom','Jour2Fête','Pan-Européenne','Cinema Public','Polygram'):
        return 1
    else:
        return 0

# 🎭 Scoring à partir des acteurs/réalisateurs
def scoring_casting(film):
    poids_total = 0
    token = st.session_state["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    noms = []

    try:
        acteurs = requests.get(f"{URL_API_CRUD}/films/{film['id_film']}/acteurs/", headers=headers).json()
        realisateurs = requests.get(f"{URL_API_CRUD}/films/{film['id_film']}/realisateurs/", headers=headers).json()
        noms = [a['nom'] for a in acteurs] + [r['nom'] for r in realisateurs]
    except:
        noms = []

    for personne in noms:
        if personne in actors_df['name'].values:
            poids = actors_df.loc[actors_df['name'] == personne, 'coef_personne'].values[0]
            poids_total += poids
            print(f"🎭 {personne} : {poids}")
    return poids_total

# 📦 Récupérer les films via l'API CRUD
def get_films_from_api():
    if not st.session_state["access_token"]:
        st.error("⚠️ Veuillez vous connecter pour accéder aux films.")
        return pd.DataFrame()

    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    try:
        response = requests.get(f"{URL_API_CRUD}/films/", headers=headers)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"⚠️ Erreur API CRUD : {response.status_code}")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Erreur de requête API CRUD : {str(e)}")
        return pd.DataFrame()

# 🧪 Nettoyage des valeurs
def safe_value(value, default):
    if value is None or pd.isna(value):
        return default
    try:
        return int(value) if isinstance(default, int) else value
    except ValueError:
        return default

# 📈 Fonction de prédiction
def get_predictions(film):
    headers = {'Content-Type': 'application/json'}
    scoring = scoring_casting(film)
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
            print(f"⚠️ Erreur API prédiction : {response.status_code} - {response.text}")
            return f"Erreur API: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erreur de requête: {str(e)}"

# 🖥️ Interface principale
st.title("🎬 Prédiction d'entrées - CinéApp")

if st.session_state["access_token"]:
    films = get_films_from_api()

    if films.empty:
        st.warning("⚠️ Aucun film trouvé.")
    else:
        st.info(f"📊 {len(films)} films récupérés.")
        films["prediction_entrees"] = films.apply(get_predictions, axis=1)

        films_sorted = films.sort_values(by="prediction_entrees", ascending=False)

        st.subheader("🎯 Top Prédictions")
        st.dataframe(films_sorted[["titre", "prediction_entrees", "budget", "studio"]])

        st.subheader("📊 Graphique")
        st.bar_chart(films_sorted.set_index("titre")["prediction_entrees"])
else:
    st.warning("⛔ Veuillez vous connecter pour voir les prédictions.")
