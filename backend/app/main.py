from fastapi import FastAPI

app = FastAPI(
    title="AI Interview Training Platform API"
)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}