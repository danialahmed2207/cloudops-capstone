# CLAUDE.md – Kontext für Claude Code

Diese Datei gibt Claude Code den Kontext für dieses Projekt. Beim Start im Terminal `claude` in diesem Ordner ausführen – Claude liest diese Datei automatisch.

## Projekt

CloudOps Capstone – Modul-4-Abschlussprojekt (Syntax Institut, Danial Ahmed). Eine kleine Web-App (Aufgaben-/Ticket-Verwaltung) mit dem Fokus auf einer vollständigen, professionellen CI/CD-Pipeline auf AWS. Das Ziel ist NICHT eine komplexe App, sondern eine saubere DevOps-Automatisierung als Vorzeige-Projekt für Bewerbungen (Junior Cloud/DevOps).

## Pflichtbausteine (müssen erfüllt sein)

- Frontend: React (Vite)
- Backend: FastAPI (Python) + DB (SQLite für MVP, RDS/PostgreSQL als Ausbau)
- DevOps: GitHub Actions + Terraform
- Hosting: AWS

## Zielarchitektur

```
git push (main)      → GitHub Actions: Tests → Build → Deploy STAGING (1 EC2)
git tag v1.x.x       → GitHub Actions: Deploy PRODUCTION (mehrere EC2)
Terraform            → VPC, Subnets, Security Groups, EC2, S3 (Remote State)
Docker               → App als Image (Multi-Stage, nginx:alpine)
Slack Webhook        → Nachricht bei Start / Success / Failure
```

## Wichtige Konventionen (aus dem Unterricht)

- Terraform-Dateien getrennt: `main.tf`, `variables.tf`, `outputs.tf`, `backend.tf`.
- Remote State im S3-Bucket (global eindeutiger Name!). `.tfstate` NIE committen.
- Test-Job als Gate: Deploy-Job nutzt `needs: <testjob>` → Deploy nur bei grünen Tests.
- Staging-Trigger: `push` auf `main`. Prod-Trigger: Tag `v*`.
- Secrets in GitHub: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `SSH_PRIVATE_KEY`, `SLACK_WEBHOOK_URL`.
- Kleinschrittig arbeiten: großes Feature in ~10 Teilaufgaben zerlegen, jeden Schritt einzeln testen.
- `terraform destroy` als manueller `workflow_dispatch`-Job → Kosten sparen (Free Tier!).

## Arbeitsreihenfolge (Vorschlag)

1. [x] Backend (FastAPI) lokal lauffähig + pytest grün
2. [x] Frontend (React/Vite) mit Anbindung ans Backend
3. [ ] Docker (Multi-Stage) für Frontend & Backend
4. [ ] Terraform-Infra lokal `plan`/`apply` testen
5. [ ] GitHub Actions Staging (Test-Gate + Deploy)
6. [ ] GitHub Actions Production (Tag `v*`) + Slack
7. [ ] Doku + Architektur-Diagramm + Kostenkapitel (für IHK-Präsentation)

## Dev-Umgebung: Stolperfallen (externe LaCie-Platte, exFAT, Doppelpunkt im Pfad)

- Python-venv liegt in `~/.venvs/cloudops-backend` (venv verweigert Pfade mit `:`).
- npm-Scripts rufen `node node_modules/vite/bin/vite.js` direkt auf (PATH bricht am `:`).
- `vite.config.js` hat `server.fs.strict: false` (Vite hält den `:`-Pfad für ein Windows-Laufwerk).
- SQLite-Engine nutzt `NullPool` (offene Handles auf exFAT werden nach ~10 s readonly).
- Details im README, Abschnitt „Besonderheiten dieser Dev-Umgebung“.

## Kosten-Hinweis

EC2 im Free Tier (t3.micro/nano), Infra nach dem Üben per `terraform destroy` abbauen.
