from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Création de l'engine SQLAlchemy pour MySQL
engine = create_engine(DATABASE_URL, echo=True)

# Vérification de la connexion à la base de données
def check_db_connection():
    try:
        with engine.connect() as conn:
            print("✅ Connexion à MySQL réussie avec SQLAlchemy !")
    except Exception as e:
        print(f"❌ Erreur de connexion à MySQL : {e}")

# Fonction pour récupérer une session de base de données
def get_db():
    with Session(engine) as session:
        yield session
