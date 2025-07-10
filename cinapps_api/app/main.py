from fastapi import FastAPI
from app.routes import films, auth, avis
from app.database import create_db_and_tables
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Cinapps API",
    description="API sécurisée avec JWT et Auth directement dans Swagger",
    version="1.0",
    openapi_tags=[
        {"name": "Auth", "description": "Authentification avec JWT"},
        {"name": "Films", "description": "Gestion des films"},
        {"name": "Avis", "description": "Avis utilisateurs sur les films"},
    ],
)

# Instrumentation Prometheus
Instrumentator().instrument(app).expose(app)

# Inclusion des routes
app.include_router(auth.router, tags=["Auth"])
app.include_router(films.router, tags=["Films"])
app.include_router(avis.router, tags=["Avis"])

# Crée les tables au démarrage si elles n’existent pas
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


#uvicorn app.main:app --reload