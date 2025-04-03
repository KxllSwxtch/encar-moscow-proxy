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


@app.post("/api/proxy")
async def proxy_post(request: Request):
    body = await request.json()

    target_url = body.get("url")
    method = body.get("method", "POST").upper()
    headers = body.get("headers", {})
    data = body.get("body", "")

    if not target_url:
        return {"error": "URL не указан"}

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=target_url,
            headers=headers,
            content=data.encode("utf-8") if isinstance(data, str) else data,
        )

        # Если ответ JSON — возвращаем его как JSON
        try:
            return JSONResponse(
                status_code=response.status_code, content=response.json()
            )
        except Exception:
            return JSONResponse(
                status_code=response.status_code, content={"text": response.text}
            )
