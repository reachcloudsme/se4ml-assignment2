import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sys

sys.modules["time_rcd"] = MagicMock()

from model.inference import calculate_anomaly_score


def test_anomaly_score():
    window = np.array(
        [
            [0.2, 100],
            [0.3, 110],
            [0.4, 120],
            [0.5, 130],
            [0.6, 140],
        ]
    )

    with patch("model.inference.detector") as mock_detector:
        mock_detector.predict.return_value = np.array([0.01234567])

        score = calculate_anomaly_score(window)

    assert score == 0.01235
    mock_detector.predict.assert_called_once()
