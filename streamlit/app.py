import streamlit as st
import pandas as pd
import requests
import os
import mysql.connector
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérifier et récupérer l'URL de l'API
URL_API = os.getenv('URL_API', 'http://127.0.0.1:8001/prediction')
if not URL_API:
    raise ValueError("L'URL de l'API n'est pas définie. Vérifie ton fichier .env")

# Fonction pour récupérer la connexion MySQL
def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            host=os.getenv('MYSQL_HOST'),
            database=os.getenv('MYSQL_DATABASE')
        )
        if conn.is_connected():
            print("✅ Connecté à MySQL")
            return conn
    except mysql.connector.Error as e:
        st.error(f"Erreur de connexion MySQL: {e}")
        return None

# Fonction pour récupérer les films depuis la base de données
def get_films():
    conn = get_mysql_connection()
    if not conn:
        return pd.DataFrame()
    
    query = """
        SELECT id_film, titre, duree, pays, studio, salles, date_sortie, budget, genre
        FROM films
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fonction pour faire les prédictions via l'API
def get_predictions(film):
    headers = {'Content-Type': 'application/json'}
    
    # Création du payload pour l'API
    data = {
        'budget': film['budget'] if pd.notna(film['budget']) else 25000000,
        'duree': film['duree'] if pd.notna(film['duree']) else 107,
        'genre': film['genre'] if pd.notna(film['genre']) else 'missing',
        'pays': film['pays'] if pd.notna(film['pays']) else 'missing',
        'salles_premiere_semaine': film['salles'] if pd.notna(film['salles']) else 100,
        'scoring_acteurs_realisateurs': 0,
        'coeff_studio': 0,
        'year': film['date_sortie'].year if pd.notna(film['date_sortie']) else 2024
    }
    
    try:
        response = requests.post(URL_API, json=data, headers=headers)
        if response.status_code == 200:
            prediction = response.json()
            return int(prediction['prediction'])
        else:
            return f"Erreur API: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erreur de requête: {str(e)}"

# Interface Streamlit
st.title("📽️ Prédiction d'entrées pour les films")

# Récupérer les films
films = get_films()

if films.empty:
    st.warning("Aucun film trouvé dans la base de données.")
else:
    # Appliquer la prédiction sur chaque film
    films["prediction_entrees"] = films.apply(get_predictions, axis=1)
    
    # Trier les films par nombre de prédictions décroissant
    films_sorted = films.sort_values(by="prediction_entrees", ascending=False)
    
    # Affichage du tableau des films
    st.write("🎬 **Top Films avec prédictions**")
    st.dataframe(films_sorted)

    # Graphique des prédictions
    st.bar_chart(films_sorted.set_index("titre")["prediction_entrees"])

