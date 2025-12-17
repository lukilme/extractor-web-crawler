FROM python:3.12-slim
WORKDIR /app
COPY ./pyproject.toml /app/
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn httpx
COPY . /app
EXPOSE 8100
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]
