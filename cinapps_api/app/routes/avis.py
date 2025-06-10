from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.models import Avis
from app.schemas import AvisCreate

router = APIRouter(prefix="/avis", tags=["Avis"])

# ➕ Créer un avis
@router.post("/avis/")
def create_avis(avis: AvisCreate, db: Session = Depends(get_db)):
    avis_model = Avis(**avis.dict())  # convertit AvisCreate en modèle SQLModel
    db.add(avis_model)
    db.commit()
    db.refresh(avis_model)
    return avis_model

# 📄 Obtenir tous les avis
@router.get("/")
def get_all_avis(db: Session = Depends(get_db)):
    return db.exec(select(Avis)).all()

# 🧾 Obtenir les avis d’un film spécifique
@router.get("/film/{film_id}")
def get_avis_by_film(film_id: int, db: Session = Depends(get_db)):
    return db.exec(select(Avis).where(Avis.id_film == film_id)).all()

# 🔄 Mettre à jour un avis
@router.put("/{avis_id}")
def update_avis(avis_id: int, updated_avis: Avis, db: Session = Depends(get_db)):
    avis = db.get(Avis, avis_id)
    if not avis:
        raise HTTPException(status_code=404, detail="Avis introuvable")
    for key, value in updated_avis.dict(exclude_unset=True).items():
        setattr(avis, key, value)
    db.commit()
    db.refresh(avis)
    return avis

# ❌ Supprimer un avis
@router.delete("/{avis_id}")
def delete_avis(avis_id: int, db: Session = Depends(get_db)):
    avis = db.get(Avis, avis_id)
    if not avis:
        raise HTTPException(status_code=404, detail="Avis introuvable")
    db.delete(avis)
    db.commit()
    return {"message": "Avis supprimé"}
