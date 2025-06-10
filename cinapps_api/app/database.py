from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os

# 🔧 Chargement des variables d'environnement (.env)
load_dotenv()

# 🔗 Connexion à la base
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# 🔍 Vérifie que la connexion fonctionne
def check_db_connection():
    try:
        with engine.connect() as conn:
            print("✅ Connexion à MySQL réussie avec SQLAlchemy !")
    except Exception as e:
        print(f"❌ Erreur de connexion à MySQL : {e}")

# 🌀 Session utilisable dans les routes
def get_db():
    with Session(engine) as session:
        yield session

import time
from sqlalchemy.exc import OperationalError

def create_db_and_tables():
    retries = 10
    for i in range(retries):
        try:
            SQLModel.metadata.create_all(engine)
            print("✅ Tables créées avec succès")
            return
        except OperationalError as e:
            print(f"⏳ Tentative {i+1}/{retries} : MySQL pas prêt → {e}")
            time.sleep(5)
    raise Exception("❌ MySQL non disponible après plusieurs tentatives.")