from fastapi import FastAPI

app = FastAPI(title="IT Challenge: обработка CSV")


@app.get("/health")
def health():
    return {"status": "ok"}