import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.integration
def test_redis_reel():
    client = TestClient(app)
    premier = client.get("/").json()["visites"]
    assert client.get("/").json()["visites"] == premier + 1
