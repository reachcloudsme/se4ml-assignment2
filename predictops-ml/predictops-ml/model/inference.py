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
        scores = detector.predict(window)
        latest_score = round(float(np.asarray(scores).reshape(-1)[-1]), 5)

        logger.info("Anomaly score calculated successfully")
        return latest_score

    except (ValueError, RuntimeError, IndexError, TypeError):
        logger.exception("Time-RCD inference failed")
        raise
