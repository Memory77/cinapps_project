from fastapi import FastAPI, Depends
from pydantic import BaseModel
from model_utils import load_model
from auth import get_current_user
import pandas as pd

app = FastAPI()
model = load_model()  #modèle ML préchargé

class FeaturesInput(BaseModel):
    budget: float
    duree: int
    genre: str
    pays: str
    salles_premiere_semaine: int
    scoring_acteurs_realisateurs: float
    coeff_studio: int
    year: int

class PredictionOutput(BaseModel):
    prediction: float

@app.post('/prediction/', response_model=PredictionOutput)
def prediction_root(
    feature_input: FeaturesInput,
    current_user: str = Depends(get_current_user)
):
    data = pd.DataFrame([{
        'budget': feature_input.budget,
        'duree': feature_input.duree,
        'genre': feature_input.genre,
        'pays': feature_input.pays,
        'salles_premiere_semaine': feature_input.salles_premiere_semaine,
        'scoring_acteurs_realisateurs': feature_input.scoring_acteurs_realisateurs,
        'coeff_studio': feature_input.coeff_studio,
        'year': feature_input.year
    }])
    
    prediction = model.predict(data)
    return PredictionOutput(prediction=prediction)





#uvicorn main:app --host 0.0.0.0 --port 8001 --reload