from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="AI Interview Training Platform API"
)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config-check")
def config_check():
    return {
        "database_configured": bool(settings.database_url),
        "jwt_configured": bool(settings.jwt_secret_key),
        "groq_configured": bool(settings.groq_api_key),
    }