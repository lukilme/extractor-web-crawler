FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY ./nlp-gateway/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

RUN ollama serve & \
    sleep 5 && \
    ollama pull phi3:3.8b

COPY ./nlp-gateway /app

EXPOSE 8100 11434

CMD ollama serve & sleep 3 && uvicorn main:app --host 0.0.0.0 --port 8100

