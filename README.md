# CloudOps Capstone

End-to-end **DevOps-Pipeline auf AWS**: eine kleine Web-App (Aufgaben-/Ticket-Verwaltung),
die über GitHub Actions automatisch getestet und ausgerollt wird – Infrastruktur per Terraform,
Auslieferung per Docker, Benachrichtigungen per Slack.

> Modul-4-Abschlussprojekt · Syntax Institut · Danial Ahmed

## Tech-Stack

| Bereich | Technologie |
|---|---|
| Frontend | React (Vite) |
| Backend | FastAPI (Python), SQLite (MVP) / PostgreSQL (RDS) |
| Infrastruktur | Terraform (VPC, EC2, S3, IAM, Security Groups) |
| CI/CD | GitHub Actions (Staging + Production) |
| Container | Docker (Multi-Stage, nginx:alpine) |
| Notifications | Slack Incoming Webhook |

## Pipeline in Kürze

- **Push auf `main`** → Tests laufen → bei Erfolg Deploy auf **Staging**.
- **Tag `v*`** (z. B. `v1.0.0`) → Deploy auf **Production**.
- Bei jedem Lauf: Slack-Nachricht (Start / Success / Failure).

## Ordnerstruktur

```
cloudops-capstone/
├── backend/            # FastAPI + pytest
├── frontend/           # React (Vite)
├── infra/              # Terraform (main/variables/outputs/backend)
├── .github/workflows/  # deploy-staging.yml, deploy-prod.yml
├── docs/               # Architektur, Kostenkapitel, Präsentation
├── CLAUDE.md           # Kontext für Claude Code
└── README.md
```

## Lokaler Start (Backend)

```bash
cd backend
# Hinweis: Das venv liegt AUSSERHALB des Projekts (~/.venvs/cloudops-backend),
# weil der Laufwerkspfad einen Doppelpunkt enthält ("Speicher: Macbook") –
# venv/npm vertragen keinen ":" im Pfad (PATH-Trennzeichen).
python3 -m venv ~/.venvs/cloudops-backend
source ~/.venvs/cloudops-backend/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload      # http://localhost:8000/docs
pytest                          # Tests ausführen
```

## Lokaler Start (Frontend)

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173 (API-Proxy → Backend :8000)
```

## Docker (lokaler Gesamtstack)

```bash
docker compose up --build      # Frontend: http://localhost:8080
```

- `backend/Dockerfile` – Python 3.12-slim, non-root, SQLite in Volume `/data`
- `frontend/Dockerfile` – Multi-Stage: Node-Build → nginx:alpine (nur statische Dateien)
- `frontend/nginx.conf` – liefert die SPA aus und proxyt `/api` zum Backend-Container

## Besonderheiten dieser Dev-Umgebung (externe LaCie-Platte)

Der Projektpfad enthält einen Doppelpunkt und die Platte ist exFAT –
drei Workarounds sind deshalb eingebaut:

1. **Python-venv außerhalb des Projekts** (`~/.venvs/cloudops-backend`), s. o.
2. **npm-Scripts rufen Vite direkt über `node` auf** (`node node_modules/vite/bin/vite.js`
   statt `vite`), weil npm das `.bin`-Verzeichnis über die PATH-Variable einbindet
   und PATH am `:` getrennt wird.
3. **SQLite mit `NullPool`** (`backend/database.py`): Auf dem exFAT-Laufwerk werden
   lange offene Datei-Handles ungültig („attempt to write a readonly database“) –
   mit einer frischen Verbindung pro Request tritt das nicht auf.

In CI (GitHub Actions) und auf EC2 sind diese Workarounds harmlos bzw. wirkungslos –
dort gibt es normale Pfade und Dateisysteme.

## Setup-Checkliste

- [x] Backend anlegen (FastAPI + pytest)
- [ ] GitHub-Repo erstellen und pushen
- [ ] GitHub Secrets setzen (AWS-Keys, SSH-Key, Slack-Webhook)
- [ ] Terraform Remote-State-Bucket-Namen in `infra/backend.tf` eintragen
- [ ] Erste EC2 für Staging bereitstellen
