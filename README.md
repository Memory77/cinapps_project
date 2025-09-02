# Cinapps Project

##  Introduction
Cinapps est une application permettant de prédire les entrées en salle de cinéma pour un film donné. 

###  **Architecture du projet**
Le projet est composé de plusieurs **composants interconnectés** :
1. **Django** (Back-end principal) → Interface et gestion des prédictions.
2. **API CRUD (FastAPI)** → Gestion des films avec authentification via JWT.
3. **API de Prédiction (FastAPI)** → Prédiction des entrées cinéma basées sur un modèle ML.
4. **Streamlit** (Interface utilisateur) → Affichage interactif des films et des prédictions.
5. **Base de données MySQL** → Stockage des films.

<img width="1090" height="472" alt="image" src="https://github.com/user-attachments/assets/8d73e32c-7c99-40cf-9078-0e440d69bf14" />

---

## 📦 **Installation et configuration**

### **1️⃣ Prérequis**
- **Python 3.10+**
- **MySQL** 
  

### **2️⃣ Cloner le projet**
```bash
git clone https://github.com/Memory77/cinapps_project.git
cd cinapps_project
```

### **3️⃣ Configurer les variables d'environnement**
Créer un fichier `.env` à la racine et ajouter :
```ini
# MySQL Database
MYSQL_USER="db_user"
MYSQL_PASSWORD="user_mdp"
MYSQL_HOST="127.0.0.1"
MYSQL_DATABASE="db_name"

# URLs des API
URL_API_CRUD="http://127.0.0.1:8000"
URL_API_PREDICTION="http://127.0.0.1:8001"
```

### **4️⃣ Installer les dépendances**
```bash
# Installer les dépendances pour Django
cd cinapps
pip install -r requirements.txt

# Installer les dépendances pour l'API CRUD
cd ../cinapps_api
pip install -r requirements.txt

# Installer les dépendances pour Streamlit
cd ../streamlit
pip install -r requirements.txt
```

---

## **Lancer les services**

### **1️⃣ Démarrer la base de données**
```bash
sudo systemctl start mysql  
```
-- Création de la table Films
CREATE TABLE Films (
    id_film INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    duree INT,
    salles INT,
    genre VARCHAR(255),
    date_sortie DATE,
    pays VARCHAR(255),
    studio VARCHAR(255),
    description TEXT,
    image VARCHAR(255),
    budget INT,
    entrees INT,
    film_url VARCHAR(255),
);

-- Création de la table Personnes (Acteurs et Réalisateurs)
CREATE TABLE Personnes (
    id_personne INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);


-- Création de la table Participations (relations entre films et personnes)
CREATE TABLE Participations (
    id_film INT,
    id_personne INT,
    role ENUM('acteur', 'realisateur') NOT NULL,
    PRIMARY KEY (id_film, id_personne, role),
    FOREIGN KEY (id_film) REFERENCES Films(id_film) ON DELETE CASCADE,
    FOREIGN KEY (id_personne) REFERENCES Personnes(id_personne) ON DELETE CASCADE
);

<img width="443" height="628" alt="image" src="https://github.com/user-attachments/assets/8677a59e-8694-4a19-b691-afd33b76117b" />


### **2️⃣ Démarrer l’API CRUD (FastAPI)**
```bash
cd cinapps_api
uvicorn app.main:app --reload
```
- Accès à la documentation Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### **3️⃣ Démarrer l’API de Prédiction**
```bash
cd cinapps_prediction
uvicorn app.main:app --reload
```
- Accès aux endpoints de prédiction sur : [http://127.0.0.1:8001](http://127.0.0.1:8001)

### **4️⃣ Démarrer Django**
```bash
cd cinapps
python manage.py runserver
```
- L’application est accessible sur : [http://127.0.0.1:8002](http://127.0.0.1:8002)

### **5️⃣ Démarrer Streamlit**
```bash
cd streamlit
streamlit run app.py
```
- L’interface utilisateur est accessible sur : [http://127.0.0.1:8501](http://127.0.0.1:8501)

---

## 🔑 **Authentification & JWT**
- **Authentification via l’API CRUD**
- Pour obtenir un **access token**, utilisez l’endpoint `/auth/token` en envoyant `{ "username": "user", "password": "pass" }`
- Utilisez ce token pour accéder aux films : **`Authorization: Bearer <TOKEN>`**

---

## 🔗 **API CRUD : Endpoints principaux**

### **📝 CRUD sur les films**
| Méthode | Endpoint        | Description |
|---------|----------------|-------------|
| `GET`   | `/films/`      | Liste des films (nécessite un JWT) |
| `POST`  | `/films/`      | Ajouter un film (JWT requis) |
| `PUT`   | `/films/{id}`  | Mettre à jour un film (JWT requis) |
| `DELETE`| `/films/{id}`  | Supprimer un film (JWT requis) |

### **🔐 Authentification**
| Méthode | Endpoint     | Description |
|---------|-------------|-------------|
| `POST`  | `/auth/token` | Obtenir un token JWT |
| `GET`   | `/users/me/`  | Récupérer l’utilisateur connecté |

---

## 🔮 **API de Prédiction : Endpoints principaux**

| Méthode | Endpoint        | Description |
|---------|----------------|-------------|
| `POST`  | `/prediction/` | Envoi des caractéristiques d’un film pour obtenir une prédiction |

Exemple de requête :
```json
{
  "budget": 50000000,
  "duree": 120,
  "genre": "Action",
  "pays": "USA",
  "salles_premiere_semaine": 350,
  "scoring_acteurs_realisateurs": 0.8,
  "coeff_studio": 1.2,
  "year": 2024
}
```

---

<img width="1008" height="574" alt="image" src="https://github.com/user-attachments/assets/e11159e6-5a24-405f-b907-e3c15743a9d7" />

## 🐳 **Déploiement avec Docker Compose**

Tous les services (Django, API CRUD, API de prédiction, MySQL, Scrapy, Streamlit) sont conteneurisés et orchestrés via Docker Compose.
Cela permet un déploiement reproductible et simplifié

## **1️⃣ Prérequis**

Docker ≥ 20.x

Docker Compose ≥ v2

## **2️⃣ Lancer l’application**
Depuis la racine du projet :
docker compose up --build -d

## **4️⃣ Arrêter les services**
docker compose down -v





