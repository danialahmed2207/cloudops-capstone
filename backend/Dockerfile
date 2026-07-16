# Backend-Image: FastAPI + Uvicorn
# Gleiche Python-Version wie in der CI (.github/workflows) → konsistente Umgebung
FROM python:3.12-slim

WORKDIR /app

# Erst nur requirements kopieren: solange sie sich nicht ändern,
# nutzt Docker den Layer-Cache und überspringt das pip install.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Nicht als root laufen; /data ist der Ablageort für die SQLite-DB (Volume)
RUN useradd --create-home appuser \
    && mkdir /data \
    && chown appuser:appuser /data
USER appuser

ENV DATABASE_URL=sqlite:////data/tasks.db

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
