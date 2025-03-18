from passlib.hash import django_pbkdf2_sha256
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# 🔐 Configuration pour pbkdf2_sha256 (compatible Django)
pwd_context = CryptContext(schemes=["django_pbkdf2_sha256"], deprecated="auto")


# 🔑 Clé secrète et algorithme pour JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def verify_password(plain_password, hashed_password):
    """Vérifie si le mot de passe correspond au hash Django pbkdf2_sha256"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print("Erreur de vérification du mot de passe :", e)
        return False

def get_password_hash(password):
    """Hash un mot de passe en Django pbkdf2_sha256"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Crée un token JWT avec une date d'expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
