# Cinapps Project

## 🚀 Introduction
Cinapps est une application permettant de prédire les entrées en salle de cinéma pour un film donné. 

### 🔹 **Architecture du projet**
Le projet est composé de plusieurs **composants interconnectés** :
1. **Django** (Back-end principal) → Interface et gestion des prédictions.
2. **API CRUD (FastAPI)** → Gestion des films avec authentification via JWT.
3. **API de Prédiction (FastAPI)** → Prédiction des entrées cinéma basées sur un modèle ML.
4. **Streamlit** (Interface utilisateur) → Affichage interactif des films et des prédictions.
5. **Base de données MySQL** → Stockage des films et des utilisateurs.

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

## 🎬 **Lancer les services**

### **1️⃣ Démarrer la base de données**
```bash
sudo systemctl start mysql  # Ou `mariadb` selon votre système
```

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

## **📊 Flux de données**
1. **L'utilisateur se connecte** et récupère un **token JWT** depuis l'API CRUD.
2. **L'API CRUD récupère les films** dans la base MySQL et les envoie à **Streamlit**.
3. **Streamlit affiche les films** et les envoie à l'**API de prédiction**.
4. **L’API de prédiction** renvoie une estimation des entrées pour chaque film.
5. **Les résultats sont affichés** dans **Streamlit** sous forme de **tableau et graphique**.

---

## 📚 **Technologies utilisées**
- **Django** (Back-end principal)
- **FastAPI** (API CRUD + API de prédiction)
- **Streamlit** (Interface utilisateur)
- **MySQL** (Base de données)
- **JWT** (Authentification sécurisée)
- **Pandas, NumPy, Scikit-Learn** (Traitement des données et ML)

---

## 🛠️ **Développement et Contribution**
1. **Forker le repo**
2. **Créer une branche** : `git checkout -b feature-nouvelle-fonctionnalité`
3. **Faire des modifications et commit** : `git commit -m "Ajout d'une nouvelle fonctionnalité"`
4. **Pusher sur GitHub** : `git push origin feature-nouvelle-fonctionnalité`
5. **Créer une Pull Request**

---

## 🔥 **TODO et améliorations possibles**
- ✅ Ajouter un **système d’authentification complet**
- ✅ Intégrer une **base de données propre**
- 🔲 Améliorer l’interface **Streamlit** (filtres, affichage des détails…)
- 🔲 Optimiser les **requêtes vers l’API de prédiction**
- 🔲 Ajouter **des tests unitaires**

---

## 🏆 **Crédits et remerciements**
Projet réalisé par **Memory77** et contributeurs ✨.
