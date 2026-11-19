from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app.models import Task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT Challenge: обработка CSV")


@app.get("/")
def root():
    return {"message": "IT Challenge API", "docs": "/docs"}


@app.get("/health")
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}