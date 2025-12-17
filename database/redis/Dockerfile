FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir celery flower redis pymongo

CMD ["celery", "--broker=redis://redis:6379/0", "flower", "--port=5555"]
