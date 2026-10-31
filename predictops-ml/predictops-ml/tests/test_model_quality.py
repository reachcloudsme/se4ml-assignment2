import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from quality.model_quality import measure_model_quality


def test_precision_recall():
    result = measure_model_quality(
        [0, 1, 1, 0, 1],
        [0, 1, 0, 1, 1],
    )

    assert result["precision"] == 0.66667
    assert result["recall"] == 0.66667


def test_perfect_predictions():
    result = measure_model_quality([0, 1, 1], [0, 1, 1])

    assert result["precision"] == 1.0
    assert result["recall"] == 1.0


def test_invalid_labels():
    with pytest.raises(ValueError):
        measure_model_quality([0, 2], [0, 1])
