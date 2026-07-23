# Lessons Learned – was auf dem Weg wirklich schiefging

Dieses Dokument sammelt die echten Probleme aus der Entwicklung, mit Original-Fehlermeldungen
und dem jeweiligen Lösungsweg. Für die Präsentation: Jede dieser Geschichten zeigt
Debugging-Vorgehen (Symptom → Hypothese → Minimal-Reproduktion → Fix).

## 1. SQLite wird nach ~10 Sekunden „readonly“ (exFAT-Laufwerk)

**Symptom:** `POST /api/tasks` lieferte `500 Internal Server Error`, obwohl alle pytest-Tests
grün waren und der Server beim Start die Tabellen anlegen konnte.

```
sqlite3.OperationalError: attempt to write a readonly database
```

**Verwirrend daran:** Ein direktes Schreiben in dieselbe Datei aus einem frischen Prozess
funktionierte problemlos. Der Fehler trat nur im laufenden Server auf.

**Minimal-Reproduktion:** `create_engine(...)` → `create_all()` → `time.sleep(10)` → INSERT
→ Fehler. Ohne die 10 Sekunden Pause: kein Fehler. Damit war klar: Nicht der Code ist kaputt,
sondern **lang offene Datei-Handles werden auf dem exFAT-Laufwerk (macOS/FSKit) ungültig**.

**Fix:** `poolclass=NullPool` in `backend/database.py` – jede Anfrage bekommt eine frische
DB-Verbindung. Bei SQLite kostet das praktisch nichts.

## 2. Doppelpunkt im Laufwerkspfad („Speicher: Macbook“) bricht das Tooling

Der Ordnername enthält `: ` – unter Unix ist `:` aber das Trennzeichen der PATH-Variable.
Drei Werkzeuge sind daran nacheinander gescheitert:

- **`python -m venv`** verweigert den Pfad komplett
  (`Refusing to create a venv ... because it contains the PATH separator :`).
  Ein Symlink ohne Doppelpunkt half nicht – venv löst den echten Pfad auf.
  → venv liegt jetzt außerhalb: `~/.venvs/cloudops-backend`.
- **`npm run dev`** fand Vite nicht (`sh: vite: command not found`), weil npm das
  Verzeichnis `node_modules/.bin` über PATH einbindet und der Eintrag am `:` zerbricht.
  → Scripts rufen `node node_modules/vite/bin/vite.js` direkt auf.
- **Vite selbst** lieferte `403 Restricted` für die eigene `index.html`, weil es den
  Doppelpunkt als Windows-Laufwerksbuchstaben fehlinterpretiert.
  → `server.fs.strict: false` (nur Dev-Server, nicht der Build).

## 3. Docker-Build bricht ab: AppleDouble-Dateien auf exFAT

**Symptom:** `docker compose build` scheiterte mit `failed to xattr ._…`-Fehlern.

**Ursache:** macOS legt auf exFAT für jede Datei eine `._*`-Schattendatei an (AppleDouble,
für erweiterte Attribute) – und zwar bei **jedem** Schreibvorgang neu. Diese Dateien
landen im Docker-Build-Kontext und bringen den Kontext-Transfer zum Absturz.

**Fix:** `scripts/docker-up.sh` räumt vor jedem Build mit `dot_clean -m .` auf.
Einmaliges Löschen reicht nicht, weil macOS die Dateien sofort wieder anlegt.

## 4. Container startet, aber die App crasht: root-only-Dateien

**Symptom:** Backend-Container beendete sich sofort mit `PermissionError` beim Start
als non-root-User.

**Ursache:** Von exFAT kopierte Dateien kommen mit Modus `700` (nur Eigentümer) ins Image.
`COPY` übernimmt sie als root-Dateien – der `appuser` darf den eigenen Code nicht lesen.

**Fix:** `COPY --chown=appuser:appuser . .` im Backend-Dockerfile.

## 5. CI: Test-Job grün, Deploy rot

Der erste GitHub-Actions-Lauf zeigt genau das Pipeline-Design: Der **test-Job läuft grün
durch** (Checkout → Python → Dependencies → pytest), der **deploy-staging-Job scheitert**,
weil die Secrets (`SLACK_WEBHOOK_URL`, `EC2_IP_STAGING`, `SSH_PRIVATE_KEY`) noch nicht
gesetzt sind. Das Test-Gate (`needs: test`) funktioniert; der Deploy wartet auf die
Infrastruktur aus Terraform. So ist der rote Lauf kein Bug, sondern der sichtbare
Zwischenstand: Anwendung fertig, Infrastruktur im Aufbau.

## Übertragbare Erkenntnisse

1. **Grüne Tests ≠ lauffähiges System.** Die Tests liefen gegen eine In-Memory-DB und
   konnten den exFAT-Fehler prinzipiell nicht sehen. Deshalb gehört zu jedem Feature ein
   echter End-to-End-Test (curl gegen den laufenden Server).
2. **Erst reproduzieren, dann fixen.** Der `sleep(10)`-Minimaltest hat aus einem
   „mysteriösen 500er“ ein klar benennbares Umgebungsproblem gemacht.
3. **Umgebung ist Teil des Systems.** Dateisystem (exFAT), Pfadnamen und Betriebssystem
   verhalten sich wie ungeschriebene Abhängigkeiten – genau darum lohnen sich Docker
   (identische Umgebung überall) und CI auf einem sauberen Runner.
