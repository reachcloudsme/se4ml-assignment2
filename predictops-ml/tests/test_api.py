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


def test_mimir_unavailable():
    from unittest.mock import patch

    import requests

    client = TestClient(app)
    with patch("app.score_service", side_effect=requests.ConnectionError("offline")):
        response = client.post("/score/api-gateway")

    assert response.status_code == 503
    assert response.json()["detail"] == "Metrics service unavailable"


def test_invalid_telemetry():
    from unittest.mock import patch

    client = TestClient(app)
    with patch("app.score_service", side_effect=ValueError("invalid data")):
        response = client.post("/score/api-gateway")

    assert response.status_code == 502
    assert response.json()["detail"] == "Invalid upstream telemetry"


def test_inference_failure():
    from unittest.mock import patch

    client = TestClient(app)
    with patch("app.score_service", side_effect=RuntimeError("detector failed")):
        response = client.post("/score/api-gateway")

    assert response.status_code == 500
    assert response.json()["detail"] == "Anomaly inference failed"


def test_missing_telemetry_warning(caplog, monkeypatch):
    import app as api

    monkeypatch.setattr(
        api,
        "query_mimir",
        lambda query, url: {"data": {"result": []}},
    )

    with caplog.at_level("WARNING"):
        result = api.score_service("api-gateway")

    assert result["status"] == "no_data"
    assert "Missing CPU or memory telemetry" in caplog.text
    assert "api-gateway" in caplog.text


def test_insufficient_telemetry_warning(caplog, monkeypatch):
    import app as api

    def mock_query(query, url):
        return {"data": {"result": [{"values": [[1, "0.2"], [2, "0.3"]]}]}}

    monkeypatch.setattr(api, "query_mimir", mock_query)

    with caplog.at_level("WARNING"):
        result = api.score_service("api-gateway")

    assert result["status"] == "insufficient_data"
    assert result["points"] == 2
    assert "Insufficient telemetry" in caplog.text
    assert "api-gateway" in caplog.text


def test_successful_scoring():
    from unittest.mock import patch

    client = TestClient(app)
    expected = {
        "service": "api-gateway",
        "anomaly_score": 0.03,
        "threshold": 0.025,
        "is_anomaly": True,
        "points": 21,
    }

    with patch("app.score_service", return_value=expected):
        response = client.post("/score/api-gateway")

    assert response.status_code == 200
    assert response.json() == expected


def test_successful_scoring_schema():
    from api_schemas import ScoreResult

    result = ScoreResult(
        service="api-gateway",
        anomaly_score=0.03,
        threshold=0.025,
        is_anomaly=True,
        points=21,
    )

    assert result.is_anomaly is True
    assert result.points == 21
