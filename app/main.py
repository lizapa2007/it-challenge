from fastapi import FastAPI, Form, HTTPException, UploadFile
from sqlalchemy import select, text

from app.database import Base, SessionLocal, engine
from app.models import Task
from app.processing import process_task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT Challenge: обработка CSV")


def task_to_dict(task: Task) -> dict:
    """Превращает задание из базы в словарь для JSON-ответа."""
    return {
        "id": task.id,
        "status": task.status,
        "filename": task.filename,
        "column": task.column_name,
        "result": task.result,
        "error": task.error,
        "created_at": task.created_at,
    }


@app.get("/")
def root():
    return {"message": "IT Challenge API", "docs": "/docs"}


@app.get("/health")
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}


@app.post("/tasks", status_code=201)
def create_task(file: UploadFile, column: str = Form()):
    content = file.file.read().decode("utf-8-sig", errors="replace")

    with SessionLocal() as db:
        task = Task(
            filename=file.filename or "file.csv",
            column_name=column,
            file_content=content,
        )
        db.add(task)
        db.commit()

        process_task(db, task)

        return task_to_dict(task)


@app.get("/tasks")
def list_tasks():
    with SessionLocal() as db:
        tasks = db.scalars(select(Task).order_by(Task.id.desc())).all()
        return [task_to_dict(task) for task in tasks]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with SessionLocal() as db:
        task = db.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        return task_to_dict(task)