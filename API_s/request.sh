#!/bin/bash

# token obtenu via l'API CRUD
TOKEN="eyJhbGciOiJIUzI1NiIsIn5cCI6IkpXVCJ9.eyJzdWIiOiJkZWJvcmFoIiwiZXhwIjoxNzQ0ODEzMTk4fQ.iggnTfZJMD1vCMYDQaEFkuGe1UG21dY-onMFY3a9FT0"

# appel à l'API de prédiction en passant le token
curl -X POST http://localhost:8001/prediction/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "budget": 25000000,
           "duree": 120,
           "genre": "Action",
           "pays": "USA",
           "salles_premiere_semaine": 450,
           "scoring_acteurs_realisateurs": 0.78,
           "coeff_studio": 3,
           "year": 2024
         }'
