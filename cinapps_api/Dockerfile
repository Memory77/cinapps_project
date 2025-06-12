FROM python:3.10-slim

# Dossier de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les packages
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port interne de l'API (utile en dev)
EXPOSE 8000

# Lancer le serveur Uvicorn sur le bon port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
