from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def send_csv(text: str, column: str):
    """Отправляет CSV-текст в POST /tasks и возвращает ответ."""
    files = {"file": ("test.csv", text.encode("utf-8"), "text/csv")}
    return client.post("/tasks", files=files, data={"column": column})


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_task_completed():
    response = send_csv("date,temperature\n2026-11-01,20\n2026-11-02,22\n", "temperature")
    assert response.status_code == 201

    task = response.json()
    assert task["status"] == "completed"
    assert task["result"] == {"count": 2, "min": 20.0, "max": 22.0, "mean": 21.0}
    assert task["error"] is None


def test_create_task_failed():
    response = send_csv("date,temperature\n2026-11-01,тепло\n", "temperature")
    task = response.json()
    assert task["status"] == "failed"
    assert "не является числом" in task["error"]


def test_get_task_by_id():
    created = send_csv("x\n1\n", "x").json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_task():
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_list_tasks():
    send_csv("x\n1\n", "x")
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 1