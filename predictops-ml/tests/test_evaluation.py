import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from quality.evaluation import evaluate_calibrator


def test_synthetic_calibrator_evaluation():
    result = evaluate_calibrator()

    assert result["evaluation_size"] == 4
    assert result["dataset_type"] == "synthetic_calibrator_only"
    assert 0 <= result["precision"] <= 1
    assert 0 <= result["recall"] <= 1
    assert (
        result["true_positives"]
        + result["false_positives"]
        + result["false_negatives"]
        + result["true_negatives"]
        == result["evaluation_size"]
    )
