from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import time
import os
import json

app = FastAPI()
OLLAMA = "http://127.0.0.1:11434"
MODEL =  "phi3:3.8b"

@app.post("/summarize")
async def summarize(payload: dict):
    text = payload.get("text")
    max_tokens = payload.get("max_tokens", 200)

    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    f"{OLLAMA}/api/generate",
                    json={
                        "model": MODEL,
                        "prompt": text,
                        "stream": True,
                    },
                ) as resp:
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        yield json.loads(line).get("response", "")
        except httpx.ConnectError:
            yield "\n[erro: ollama indisponível]\n"


    return StreamingResponse(
        stream_generator(),
        media_type="text/plain"
    )

@app.post("/sum")
def sum_value(data: dict):
    print(data)
    try:
        time.sleep(2)
        value = int(data.get("value"))
    except (TypeError, ValueError):
        return {"error": "invalid value"}

    return {"result": value + 1}