FROM python:3.10-slim

WORKDIR /app

# --- 🔐 Variables
ARG SECRET_KEY
ARG ALGORITHM
ARG ACCESS_TOKEN_EXPIRE_MINUTES
ARG DATABASE_URL

ENV SECRET_KEY=$SECRET_KEY \
    ALGORITHM=$ALGORITHM \
    ACCESS_TOKEN_EXPIRE_MINUTES=$ACCESS_TOKEN_EXPIRE_MINUTES \
    DATABASE_URL=$DATABASE_URL

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
