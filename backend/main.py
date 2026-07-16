"""CloudOps Capstone – Backend (FastAPI).

Aufgaben-/Ticket-Verwaltung mit CRUD-Endpunkten unter /api/...
Start lokal:  uvicorn main:app --reload   → http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Task, TaskCreate, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="CloudOps Capstone API", version="0.1.0", lifespan=lifespan)

# CORS: erlaubt dem Vite-Dev-Server (Port 5173) Zugriff aufs Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Health-Endpunkt – nutzen später auch Load Balancer / Monitoring."""
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[Task])
def list_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task).order_by(Task.id)).all()


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    task = Task.model_validate(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task nicht gefunden")
    return task


@app.patch("/api/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int, task_in: TaskUpdate, session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task nicht gefunden")
    updates = task_in.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task nicht gefunden")
    session.delete(task)
    session.commit()
