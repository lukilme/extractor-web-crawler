FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential libpq-dev curl git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copia o requirements gerado pelo poetry export
COPY ./api/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt

# copia código
COPY ./api /app

EXPOSE 8000


CMD ["bash", "-lc", "celery -A project_name beat --loglevel=info"]
