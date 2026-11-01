import numpy as np
from model.training import train_calibrator

from quality.model_quality import measure_model_quality


def evaluate_calibrator():
    # Synthetic training data, not actual Time-RCD outputs.
    train_scores = np.array([-3, -2, -1, 1, 2, 3], dtype=float)
    train_labels = np.array([0, 0, 0, 1, 1, 1])

    # Separate synthetic holdout examples.
    test_scores = np.array([-2.5, -0.5, 0.5, 2.5], dtype=float)
    test_labels = np.array([0, 0, 1, 1])

    model = train_calibrator(train_scores, train_labels)
    predictions = model.predict(test_scores.reshape(-1, 1))

    metrics = measure_model_quality(test_labels, predictions)
    metrics["true_negatives"] = int(((test_labels == 0) & (predictions == 0)).sum())
    metrics["evaluation_size"] = len(test_labels)
    metrics["dataset_type"] = "synthetic_calibrator_only"

    return metrics


if __name__ == "__main__":
    print(evaluate_calibrator())
