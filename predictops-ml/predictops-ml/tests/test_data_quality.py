import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from quality.data_quality import measure_data_quality


def test_complete_data():
    window = np.ones((21, 2))
    result = measure_data_quality(window)

    assert result["missing_rate"] == 0
    assert result["completeness"] == 1.0


def test_missing_data():
    window = np.array([[0.2, 100], [np.nan, 110]])
    result = measure_data_quality(window)

    assert result["missing_values"] == 1
    assert result["missing_rate"] == 0.25


def test_invalid_shape():
    with pytest.raises(ValueError):
        measure_data_quality([[1, 2, 3]])
