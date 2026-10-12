# Visites — API de comptage (version B réconciliée)

API FastAPI qui compte les visites dans Redis et expose des métriques Prometheus.

## Lancer en local

    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"
    docker run -d --name redis -p 6379:6379 redis:8-alpine
    pytest -q
    uvicorn app.main:app --reload

## Endpoints

- `GET /` : incrémente et renvoie le compteur
- `GET /health` : état de l'API et de Redis
- `GET /metrics` : métriques Prometheus
