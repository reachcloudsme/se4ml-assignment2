import numpy as np


def measure_model_quality(actual, predicted):
    actual = np.asarray(actual, dtype=int)
    predicted = np.asarray(predicted, dtype=int)

    if actual.shape != predicted.shape or actual.ndim != 1:
        raise ValueError("Actual and predicted labels must match")

    if actual.size == 0:
        raise ValueError("Evaluation dataset cannot be empty")

    if not np.isin(actual, [0, 1]).all() or not np.isin(predicted, [0, 1]).all():
        raise ValueError("Labels must be 0 or 1")

    tp = int(((actual == 1) & (predicted == 1)).sum())
    fp = int(((actual == 0) & (predicted == 1)).sum())
    fn = int(((actual == 1) & (predicted == 0)).sum())

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {
        "precision": round(precision, 5),
        "recall": round(recall, 5),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
    }
