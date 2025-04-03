import httpx

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    target_url = request.query_params.get("url")
    if not target_url:
        return {"error": "URL не указан"}

    body = await request.body()
    headers = dict(request.headers)

    async with httpx.AsyncClient(follow_redirects=False) as client:
        try:
            response = await client.post(target_url, headers=headers, content=body)

            # Попробуем вернуть JSON, если доступно
            try:
                return JSONResponse(
                    status_code=response.status_code, content=response.json()
                )
            except Exception:
                return JSONResponse(
                    status_code=response.status_code, content={"text": response.text}
                )

        except httpx.TooManyRedirects:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Слишком много редиректов. Проверь URL или метод запроса."
                },
            )
