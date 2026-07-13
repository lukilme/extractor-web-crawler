FROM python:3.12-slim

WORKDIR /app

COPY ./nlp-gateway/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]