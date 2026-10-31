import sys
from pathlib import Path
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

sys.modules["time_rcd"] = MagicMock()

from app import app


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["namespace"] == "banking-app"
    assert len(response.json()["services"]) == 8


def test_unknown_service():
    client = TestClient(app)
    response = client.post("/score/unknown-service")

    assert response.status_code == 404
    assert response.json()["detail"] == "Unknown service"
