import redis

from app import main


def test_root_incremente(client):
    assert client.get("/").json() == {"visites": 1}
    assert client.get("/").json() == {"visites": 2}


def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_redis_absent(client, monkeypatch):
    def ping_en_panne():
        raise redis.exceptions.ConnectionError

    monkeypatch.setattr(main.r, "ping", ping_en_panne)
    assert client.get("/health").status_code == 503


def test_metrics(client):
    client.get("/")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "http_requests_total" in resp.text


def test_reset_remet_le_compteur_a_zero(client):
    client.get("/")
    client.get("/")

    resp = client.post("/reset")
    assert resp.status_code == 200
    assert resp.json() == {"visites": 0}

    assert client.get("/").json() == {"visites": 1}
