# Architektur & Kosten (für die IHK-Präsentation)

## Architektur-Überblick

```
Entwickler
   │  git push (main)                 git tag v1.x.x
   ▼                                       ▼
GitHub Actions: Test ─► Deploy STAGING   GitHub Actions: Test ─► Deploy PRODUCTION
   │  (1 EC2)                              │  (mehrere EC2, Schleife über IPs)
   ▼                                       ▼
        Terraform provisioniert: VPC · Subnets · Security Groups · EC2 · S3 (Remote State)
        Docker liefert die App aus (Multi-Stage, nginx:alpine)
        Slack meldet: Start / Success / Failure
```

> Diagramm sauber nachzeichnen mit Excalidraw, Draw.io oder Eraser.io (KI-gestützt).

## Kosten-Argumentation (Business-Fokus)

- **Free Tier:** EC2 t3.micro/nano decken den MVP kostenlos ab.
- **Kostenkontrolle:** Infra per `terraform destroy` abbauen, wenn nicht genutzt.
- **Serverless-Vergleich:** Lambda/Fargate = AWS patcht selbst (weniger Betriebsaufwand),
  EC2 = Shared Responsibility (du patchst mit). Trade-off je nach Last.
- **Anbieter-Vergleich:** AWS vs. Hetzner – Datenübertragung ist bei AWS ein Kostenpunkt;
  ehrliche Abwägung zeigt Reife.

## Präsentations-Hook (Demo)

Bug einbauen → Tests schlagen fehl → Deploy wird übersprungen (Slack: Failure).
Bug fixen → Tests grün → Auto-Deploy → Seite live.
Aussage: „So verhindert Automatisierung fehlerhafte Releases in Produktion."
