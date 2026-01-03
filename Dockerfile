FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sh -c "\
echo 'Starting web container...' && \
python wait_for_db.py && \
echo 'DB settings:' && \
python -c \"import os; \
print('DB_HOST=', os.getenv('DB_HOST')); \
print('POSTGRES_DB=', os.getenv('POSTGRES_DB')); \
print('POSTGRES_USER=', os.getenv('POSTGRES_USER'))\" && \
python manage.py migrate --noinput && \
echo 'Starting Django server...' && \
python manage.py runserver 0.0.0.0:8000 \
"



