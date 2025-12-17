from fastapi import FastAPI
import httpx
import os

app = FastAPI()
OLLAMA = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

@app.post("/summarize")
async def summarize(payload: dict):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{OLLAMA}/api/generate", json={
            "model": "ggml-model-name",
            "prompt": payload.get("text"),
            "max_length": payload.get("max_tokens", 200)
        })
        r.raise_for_status()
        return r.json()
