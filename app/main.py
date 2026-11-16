from fastapi import FastAPI

app = FastAPI(title="IT Challenge: обработка CSV")


@app.get("/")
def root():
    return {"message": "IT Challenge API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}