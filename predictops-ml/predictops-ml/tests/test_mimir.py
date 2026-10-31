import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data.mimir import query_mimir


def test_query_mimir_success():
    fake_response = Mock()
    fake_response.json.return_value = {"data": {"result": []}}

    with patch("data.mimir.requests.get", return_value=fake_response) as mock_get:
        result = query_mimir("up", "http://test-mimir")

    assert result == {"data": {"result": []}}
    mock_get.assert_called_once()


def test_query_mimir_connection_error():
    with patch(
        "data.mimir.requests.get",
        side_effect=requests.ConnectionError("Mimir unavailable"),
    ), pytest.raises(requests.ConnectionError):
        query_mimir("up", "http://test-mimir")
