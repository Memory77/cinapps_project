from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class Film(SQLModel, table=True):
    __tablename__ = "films"

    id_film: Optional[int] = Field(default=None, primary_key=True)
    titre: str
    duree: Optional[int] = None
    salles: Optional[int] = None
    genre: Optional[str] = None
    date_sortie: Optional[date] = None  #  Change `str` en `date`
    pays: Optional[str] = None
    studio: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    budget: Optional[int] = None
    entrees: Optional[int] = None
    anecdotes: Optional[str] = None
    film_url: Optional[str] = None
    is_pred: Optional[bool] = None

class User(SQLModel, table=True):
    __tablename__ = "main_user"  # On utilise la table existante

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str  # Contient déjà le mot de passe haché

class Personne(SQLModel, table=True):
    __tablename__ = "Personnes"

    id_personne: Optional[int] = Field(default=None, primary_key=True)
    nom: str

class Participation(SQLModel, table=True):
    __tablename__ = "Participations"

    id_film: int = Field(foreign_key="films.id_film", primary_key=True)
    id_personne: int = Field(foreign_key="Personnes.id_personne", primary_key=True)
    role: str  # 'acteur' ou 'realisateur'
