import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import log_loss

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.training import prepare_training_data, train_calibrator


def test_training_reduces_loss():
    # Deliberately separable synthetic anomaly scores.
    scores = np.array([-3, -2, -1, 1, 2, 3], dtype=float)
    labels = np.array([0, 0, 0, 1, 1, 1])

    features, targets = prepare_training_data(scores, labels)

    initial_probabilities = np.full(len(targets), 0.5)
    initial_loss = log_loss(targets, initial_probabilities)

    model = train_calibrator(scores, labels)
    trained_probabilities = model.predict_proba(features)[:, 1]
    trained_loss = log_loss(targets, trained_probabilities)

    print(f"\nInitial loss: {initial_loss:.5f}")
    print(f"Trained loss: {trained_loss:.5f}")

    assert trained_loss < initial_loss
    assert np.array_equal(model.predict(features), targets)


def test_training_rejects_single_class():
    scores = [0.01, 0.02, 0.03]
    labels = [0, 0, 0]

    try:
        train_calibrator(scores, labels)
    except ValueError as exc:
        assert "both normal and anomaly" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
