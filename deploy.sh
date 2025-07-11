#!/bin/bash

set -euo pipefail

# 🌍 Config
AZURE_RG="cinapps-rg"
AZURE_LOCATION="francecentral"
IMAGE_TAG="latest"

: "${DOCKERHUB_USERNAME:?DOCKERHUB_USERNAME non défini}"
: "${DOCKERHUB_TOKEN:?DOCKERHUB_TOKEN non défini}"

: "${MYSQL_USER:?}"
: "${MYSQL_PASSWORD:?}"
: "${MYSQL_DATABASE:?}"

# 🔁 Retry wrapper
retry_az_create() {
  local retries=5
  local wait=15
  local count=0

  until "$@"; do
    exit_code=$?
    count=$((count + 1))
    if [ $count -lt $retries ]; then
      echo "⏳ Retry $count... Attente $waits"
      sleep $wait
    else
      echo "❌ Échec après $retries tentatives"
      return $exit_code
    fi
  done
}

# 🔍 Vérif images Docker
IMAGES=(
  "$DOCKERHUB_USERNAME/mysql_custom:$IMAGE_TAG"
  "$DOCKERHUB_USERNAME/cinapps_api:$IMAGE_TAG"
  "$DOCKERHUB_USERNAME/api_prediction:$IMAGE_TAG"
  "$DOCKERHUB_USERNAME/cinapps:$IMAGE_TAG"
  "$DOCKERHUB_USERNAME/scrapy_crawler:$IMAGE_TAG"
  "$DOCKERHUB_USERNAME/scrapy_cron:$IMAGE_TAG"
)

for img in "${IMAGES[@]}"; do
  echo "🔍 Check image $img"
  docker manifest inspect "$img" > /dev/null || { echo "❌ Manifeste introuvable : $img"; exit 1; }
done

echo "🔐 Connexion Docker Hub"
echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

# 🧱 MySQL
echo "🧱 Déploiement MySQL..."
retry_az_create az container create \
  --resource-group "$AZURE_RG" \
  --name mysql-db \
  --image "$DOCKERHUB_USERNAME/mysql_custom:$IMAGE_TAG" \
  --cpu 1 \
  --memory 1.5 \
  --os-type Linux \
  --ports 3306 \
  --dns-name-label mysql-db-$(date +%s) \
  --environment-variables \
    MYSQL_ROOT_PASSWORD="$MYSQL_PASSWORD" \
    MYSQL_DATABASE="$MYSQL_DATABASE" \
    MYSQL_USER="$MYSQL_USER" \
    MYSQL_PASSWORD="$MYSQL_PASSWORD" \
  --registry-login-server index.docker.io \
  --registry-username "$DOCKERHUB_USERNAME" \
  --registry-password "$DOCKERHUB_PASSWORD"

echo "⏳ Attente 30s pour MySQL..."
sleep 30

MYSQL_HOST=$(az container show \
  --resource-group "$AZURE_RG" \
  --name mysql-db \
  --query ipAddress.fqdn \
  --output tsv)

echo "✅ MySQL lancé sur $MYSQL_HOST"

# 🚀 CRUD API
echo "🚀 Déploiement CRUD API..."
retry_az_create az container create \
  --resource-group "$AZURE_RG" \
  --name cinapps-api \
  --image "$DOCKERHUB_USERNAME/cinapps_api:$IMAGE_TAG" \
  --cpu 1 \
  --memory 1.5 \
  --os-type Linux \
  --ports 8000 \
  --dns-name-label crud-api-$(date +%s) \
  --environment-variables \
    SECRET_KEY="$SECRET_KEY" \
    ALGORITHM="$ALGORITHM" \
    ACCESS_TOKEN_EXPIRE_MINUTES="$ACCESS_TOKEN_EXPIRE_MINUTES" \
    DATABASE_URL="mysql+mysqlconnector://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST:$MYSQL_PORT/$MYSQL_DATABASE"

# 🔮 Prédiction API
echo "🔮 Déploiement API Prédiction..."
retry_az_create az container create \
  --resource-group "$AZURE_RG" \
  --name api-prediction \
  --image "$DOCKERHUB_USERNAME/api_prediction:$IMAGE_TAG" \
  --cpu 1 \
  --memory 1.5 \
  --os-type Linux \
  --ports 8001 \
  --dns-name-label pred-api-$(date +%s) \
  --environment-variables \
    SECRET_KEY="$SECRET_KEY" \
    ALGORITHM="$ALGORITHM" \
    URL_API="$URL_API" \
    MYSQL_HOST="$MYSQL_HOST" \
    MYSQL_USER="$MYSQL_USER" \
    MYSQL_PASSWORD="$MYSQL_PASSWORD" \
    MYSQL_DATABASE="$MYSQL_DATABASE"

# 🎬 Front Django
echo "🎬 Déploiement Front..."
retry_az_create az container create \
  --resource-group "$AZURE_RG" \
  --name cinapps-front \
  --image "$DOCKERHUB_USERNAME/cinapps:$IMAGE_TAG" \
  --cpu 1 \
  --memory 1.5 \
  --os-type Linux \
  --ports 8002 \
  --dns-name-label cinapps-front-$(date +%s) \
  --environment-variables \
    SECRET_KEY="$SECRET_KEY" \
    DEBUG="$DEBUG" \
    API_CRUD_URL="http://cinapps-api:8000" \
    API_CRUD_USERNAME="$API_CRUD_USERNAME" \
    API_CRUD_PASSWORD="$API_CRUD_PASSWORD" \
    URL_API="$URL_API" \
    MYSQL_HOST="$MYSQL_HOST" \
    MYSQL_USER="$MYSQL_USER" \
    MYSQL_PASSWORD="$MYSQL_PASSWORD" \
    MYSQL_DATABASE="$MYSQL_DATABASE" \
    MYSQL_PORT="$MYSQL_PORT" \
    MYSQL_RDY=1

# 🕷️ Scrapy
echo "🕷️ Déploiement Scrapy..."
retry_az_create az container create \
  --resource-group "$AZURE_RG" \
  --name scrapy-crawler \
  --image "$DOCKERHUB_USERNAME/scrapy_crawler:$IMAGE_TAG" \
  --cpu 1 \
  --memory 1.0 \
  --os-type Linux \
  --dns-name-label crawler-$(date +%s) \
  --environment-variables \
    MYSQL_HOST="$MYSQL_HOST" \
    MYSQL_USER="$MYSQL_USER" \
    MYSQL_PASSWORD="$MYSQL_PASSWORD" \
    MYSQL_DATABASE="$MYSQL_DATABASE"

# ⏱️ Cron
echo "⏱️ Déploiement Cron Scrapy..."
retry_az_create az container create \
  --resource-group "$AZURE_RG" \
  --name scrapy-cron \
  --image "$DOCKERHUB_USERNAME/scrapy_cron:$IMAGE_TAG" \
  --cpu 1 \
  --memory 1.0 \
  --os-type Linux \
  --dns-name-label cronjob-$(date +%s) \
  --environment-variables \
    MYSQL_HOST="$MYSQL_HOST" \
    MYSQL_USER="$MYSQL_USER" \
    MYSQL_PASSWORD="$MYSQL_PASSWORD" \
    MYSQL_DATABASE="$MYSQL_DATABASE"

echo "🎉 Déploiement terminé avec succès !"
