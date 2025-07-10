FROM python:3.10-slim

WORKDIR /app

# --- 🔐 Variables passées via GitHub Actions
ARG SECRET_KEY
ARG ALGORITHM
ARG URL_API
ARG MYSQL_HOST
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_DATABASE

ENV SECRET_KEY=$SECRET_KEY \
    ALGORITHM=$ALGORITHM \
    URL_API=$URL_API \
    MYSQL_HOST=$MYSQL_HOST \
    MYSQL_USER=$MYSQL_USER \
    MYSQL_PASSWORD=$MYSQL_PASSWORD \
    MYSQL_DATABASE=$MYSQL_DATABASE

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
