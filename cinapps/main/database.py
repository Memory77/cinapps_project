from dotenv import load_dotenv
import mysql.connector
import os

# Charger les variables d'environnement
load_dotenv()

def get_mysql_connection():
    try:
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')
        host = os.getenv('MYSQL_HOST')
        database = os.getenv('MYSQL_DATABASE')
        
        # Vérification des variables d'environnement
        print(f'USER: {user}, PASSWORD: {password}, HOST: {host}, DATABASE: {database}')
        
        conn = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database,
            buffered=True
        )
        
        if conn.is_connected():
            print('Connecté à la base de données MySQL')
            return conn
    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données MySQL: {e}")
        return None

def get_directors_by_film(conn, film_id):
    directors = []
    query = """
    SELECT p.id_personne, p.nom 
    FROM Personnes p
    JOIN Participations part ON p.id_personne = part.id_personne
    JOIN films f ON part.id_film = f.id_film
    WHERE f.id_film = %s AND part.role = 'realisateur';
    """
    cursor = None  # ✅ Déclare cursor ici
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (film_id,))
        directors = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Erreur lors de la récupération des réalisateurs: {e}")
    finally:
        if cursor:
            cursor.close()  # ✅ Fermer le curseur même en cas d'erreur
    return directors


def get_actors_by_film(conn, film_id):
    actors = []
    query = """
    SELECT p.id_personne, p.nom 
    FROM Personnes p
    JOIN Participations part ON p.id_personne = part.id_personne
    JOIN films f ON part.id_film = f.id_film
    WHERE f.id_film = %s AND part.role = 'acteur';
    """
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (film_id,))
        actors = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Erreur lors de la récupération des acteurs: {e}")
    finally:
        if cursor:
            cursor.close()  # ✅ Fermer proprement
    return actors

