#!/usr/bin/env bash
# Baut und startet den Docker-Stack.
# Räumt vorher die macOS-AppleDouble-Dateien (._*) weg, die auf der
# exFAT-Platte bei jedem Schreibvorgang entstehen und den Docker-Build
# mit "failed to xattr ._..." abbrechen lassen.
set -euo pipefail
cd "$(dirname "$0")/.."
dot_clean -m . 2>/dev/null || true
docker compose up -d --build "$@"
docker compose ps
