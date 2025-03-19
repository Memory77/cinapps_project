from fastapi import FastAPI
from app.routes import films, auth

app = FastAPI(
    title="Cinapps API",
    description="API sécurisée avec JWT et Auth directement dans Swagger",
    version="1.0",
    openapi_tags=[
        {"name": "Auth", "description": "Authentification avec JWT"},
        {"name": "Films", "description": "Gestion des films"},
    ],
)

# 🔄 Inclusion des routes
app.include_router(auth.router, tags=["Auth"])
app.include_router(films.router, tags=["Films"])

#uvicorn app.main:app --reload