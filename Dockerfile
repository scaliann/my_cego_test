FROM python:3.10-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .


EXPOSE 8000

CMD ["gunicorn", "yadisk_app.wsgi:application", "--bind", "0.0.0.0:8000"]
