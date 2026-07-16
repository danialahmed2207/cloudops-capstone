"""API-Tests für das Backend.

Wichtig: Die Tests laufen gegen eine In-Memory-SQLite (nicht gegen tasks.db).
Dazu überschreiben wir die get_session-Dependency der App – so testen wir
die echten Routen, aber mit einer frischen Wegwerf-Datenbank pro Test.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from database import get_session
from main import app


@pytest.fixture(name="client")
def client_fixture():
    # StaticPool: alle Verbindungen teilen sich dieselbe In-Memory-DB
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task(client):
    response = client.post("/api/tasks", json={"title": "Terraform lernen"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Terraform lernen"
    assert data["status"] == "open"
    assert data["id"] == 1
    assert data["created_at"] is not None


def test_create_task_without_title_fails(client):
    response = client.post("/api/tasks", json={"description": "ohne Titel"})
    assert response.status_code == 422


def test_list_tasks(client):
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})
    response = client.get("/api/tasks")
    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["Task 1", "Task 2"]


def test_get_task(client):
    created = client.post("/api/tasks", json={"title": "Einzelner Task"}).json()
    response = client.get(f"/api/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Einzelner Task"


def test_get_task_not_found(client):
    response = client.get("/api/tasks/999")
    assert response.status_code == 404


def test_update_task_status(client):
    created = client.post("/api/tasks", json={"title": "Status ändern"}).json()
    response = client.patch(
        f"/api/tasks/{created['id']}", json={"status": "done"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"
    # Titel bleibt unverändert (PATCH = nur geschickte Felder ändern)
    assert response.json()["title"] == "Status ändern"


def test_update_task_invalid_status(client):
    created = client.post("/api/tasks", json={"title": "Task"}).json()
    response = client.patch(
        f"/api/tasks/{created['id']}", json={"status": "erledigt"}
    )
    assert response.status_code == 422


def test_delete_task(client):
    created = client.post("/api/tasks", json={"title": "Wegwerf-Task"}).json()
    response = client.delete(f"/api/tasks/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
