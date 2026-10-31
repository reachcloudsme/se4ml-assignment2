import logging

import numpy as np
from time_rcd import TimeRCDDetector

logger = logging.getLogger(__name__)

detector = TimeRCDDetector.from_pretrained(
    variant="multi",
    device="cpu",
)


def calculate_anomaly_score(window):
    logger.info("Running Time-RCD anomaly detection")

    try:
        data = np.asarray(window, dtype=float)
        if data.ndim != 2 or data.shape[1] != 2 or data.shape[0] < 5:
            raise ValueError("Expected at least 5 rows with CPU and memory columns")
        if not np.isfinite(data).all():
            raise ValueError("Telemetry contains NaN or infinite values")

        scores = np.asarray(detector.predict(data))
        if scores.size == 0 or not np.isfinite(scores).all():
            raise ValueError("Detector returned empty or non-finite scores")
        latest_score = round(float(np.asarray(scores).reshape(-1)[-1]), 5)

        logger.info("Anomaly score calculated successfully")
        return latest_score

    except (ValueError, RuntimeError, IndexError, TypeError):
        logger.exception("Time-RCD inference failed")
        raise
