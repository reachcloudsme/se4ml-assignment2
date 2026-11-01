import logging

import numpy as np
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)


def prepare_training_data(scores, labels):
    scores = np.asarray(scores, dtype=float).reshape(-1, 1)
    labels = np.asarray(labels)

    if scores.shape[0] != labels.size or scores.shape[0] == 0:
        raise ValueError("Scores and labels must have matching non-empty lengths")

    if not np.isfinite(scores).all():
        raise ValueError("Scores must be finite")

    if not np.isin(labels, [0, 1]).all():
        raise ValueError("Labels must be binary")

    if np.unique(labels).size < 2:
        raise ValueError("Training requires both normal and anomaly examples")

    return scores, labels.astype(int)


def train_calibrator(scores, labels):
    features, targets = prepare_training_data(scores, labels)

    logger.info("Training anomaly-score calibrator on %d examples", len(targets))

    model = LogisticRegression(max_iter=1000, C=1000)
    model.fit(features, targets)

    logger.info("Calibration training completed")
    return model
