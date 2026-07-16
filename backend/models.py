"""Datenmodelle für die Aufgaben-/Ticket-Verwaltung.

SQLModel kombiniert Pydantic (Validierung) und SQLAlchemy (DB-Tabellen):
- Task        → die DB-Tabelle
- TaskCreate  → was der Client beim Anlegen schicken darf
- TaskUpdate  → was der Client beim Ändern schicken darf (alles optional)
"""

from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    status: TaskStatus = TaskStatus.OPEN


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None
