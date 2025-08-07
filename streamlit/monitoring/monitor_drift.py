import pandas as pd
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import scoring_casting, get_studio_coefficient

# 📂 Chemins
REF_PATH = "monitoring/reference.csv"
CUR_PATH = "monitoring/current.csv"
REPORT_PATH = "monitoring/report/report.html"
COEFF_PATH = "acteurs_coef.csv"

# ✅ Colonnes nécessaires à la prédiction
PREDICTION_COLUMNS = [
    "budget",
    "duree",
    "genre",
    "pays",
    "salles_premiere_semaine",
    "scoring_acteurs_realisateurs",
    "coeff_studio",
    "year"
]

def generate_drift_report():
    print("🚀 Lancement du monitoring...")

    if not os.path.exists(REF_PATH) or not os.path.exists(CUR_PATH):
        print("❌ Les fichiers reference.csv ou current.csv sont introuvables.")
        return False

    reference = pd.read_csv(REF_PATH)
    current = pd.read_csv(CUR_PATH, dtype=str)
    actors_df = pd.read_csv(COEFF_PATH)

    print(f"📊 Reference shape: {reference.shape}")
    print(f"📊 Current shape: {current.shape}")

    # Supprimer les colonnes complètement vides dans current
    empty_cols = [col for col in current.columns if current[col].isna().all()]
    if empty_cols:
        print(f"🧹 Colonnes vides retirées de current : {empty_cols}")
        current = current.drop(columns=empty_cols)

    # ➕ Ajouter colonnes manquantes
    if 'coeff_studio' not in current.columns and 'studio' in current.columns:
        current['coeff_studio'] = current['studio'].apply(lambda x: get_studio_coefficient(str(x)))

    if 'scoring_acteurs_realisateurs' not in current.columns and 'acteurs' in current.columns:
        current["scoring_acteurs_realisateurs"] = current.apply(lambda row: scoring_casting(row, actors_df), axis=1)

    # ✂️ Crop datasets
    reference_cropped = reference.copy()
    current_cropped = current.copy()

    # Convertir toutes les colonnes nécessaires en numérique
    for col in PREDICTION_COLUMNS:
        if col in reference_cropped.columns:
            reference_cropped[col] = pd.to_numeric(reference_cropped[col], errors="coerce")
        if col in current_cropped.columns:
            current_cropped[col] = pd.to_numeric(current_cropped[col], errors="coerce")

    # Ne garder que les colonnes valides (présentes + non vides dans les deux)
    valid_columns = []
    for col in PREDICTION_COLUMNS:
        if (
            col in reference_cropped.columns and
            col in current_cropped.columns and
            reference_cropped[col].notna().any() and
            current_cropped[col].notna().any()
        ):
            valid_columns.append(col)

    if not valid_columns:
        print("❌ Aucune colonne valide pour le monitoring.")
        return False

    print(f"✅ Colonnes utilisées pour le drift : {valid_columns}")
    reference_final = reference_cropped[valid_columns]
    current_final = current_cropped[valid_columns]

    # Générer le rapport
    try:
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=reference_final, current_data=current_final)
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
        report.save_html(REPORT_PATH)
        print("✅ Rapport Evidently généré avec succès.")
        return True

    except Exception as e:
        print(f"❌ Erreur Evidently: {e}")
        return False

if __name__ == "__main__":
    generate_drift_report()
