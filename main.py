from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS: Разрешим фронтенд
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/proxy")
async def proxy_get(request: Request):
    target_url = request.query_params.get("url")
    if not target_url:
        return {"error": "URL не указан"}

    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)
        return response.json()
