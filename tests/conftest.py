import fakeredis
import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "r", fakeredis.FakeRedis(decode_responses=True))
    return TestClient(main.app)
