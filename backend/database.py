"""Datenbank-Setup: SQLite für das MVP, später austauschbar gegen PostgreSQL (RDS).

Die DB-URL kommt aus der Umgebungsvariable DATABASE_URL, damit wir in
Docker/AWS ohne Codeänderung auf eine andere Datenbank zeigen können.
"""

import os

from sqlalchemy.pool import NullPool
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

if DATABASE_URL.startswith("sqlite"):
    # check_same_thread=False: FastAPI bedient Requests aus mehreren Threads.
    # NullPool: pro Request eine frische Verbindung statt Connection-Pooling –
    # bei SQLite quasi kostenlos und robust gegen Dateisystem-Eigenheiten
    # (z. B. veraltende File-Handles auf externen exFAT-Laufwerken).
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
    )
else:
    engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI-Dependency: liefert pro Request eine DB-Session."""
    with Session(engine) as session:
        yield session
