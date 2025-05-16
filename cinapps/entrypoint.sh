#!/bin/sh

set -e

echo "📡 Attente de la base de données MySQL..."

# Attente active tant que la BDD n’est pas prête
while ! nc -z "$MYSQL_HOST" "${MYSQL_PORT:-3306}"; do
  echo "⏳ En attente de MySQL à $MYSQL_HOST:${MYSQL_PORT:-3306}..."
  sleep 1
done

echo "✅ Base disponible. Migrations..."

python manage.py makemigrations
python manage.py migrate --no-input --fake-initial

echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🚀 Démarrage du serveur Django avec Gunicorn..."
#gunicorn cinapps.wsgi:application --workers=4 --bind=0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000