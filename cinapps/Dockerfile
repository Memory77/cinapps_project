FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gcc \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev

WORKDIR /app

# --- 🔐 Variables Django
ARG SECRET_KEY
ARG DEBUG
ARG API_CRUD_URL
ARG API_CRUD_USERNAME
ARG API_CRUD_PASSWORD
ARG URL_API
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_DATABASE
ARG MYSQL_HOST
ARG MYSQL_PORT
ARG MYSQL_RDY

ENV SECRET_KEY=$SECRET_KEY \
    DEBUG=$DEBUG \
    API_CRUD_URL=$API_CRUD_URL \
    API_CRUD_USERNAME=$API_CRUD_USERNAME \
    API_CRUD_PASSWORD=$API_CRUD_PASSWORD \
    URL_API=$URL_API \
    MYSQL_USER=$MYSQL_USER \
    MYSQL_PASSWORD=$MYSQL_PASSWORD \
    MYSQL_DATABASE=$MYSQL_DATABASE \
    MYSQL_HOST=$MYSQL_HOST \
    MYSQL_PORT=$MYSQL_PORT \
    MYSQL_RDY=$MYSQL_RDY

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
