import numpy as np


def measure_data_quality(window, expected_points=21):
    data = np.asarray(window, dtype=float)

    if data.ndim != 2 or data.shape[1] != 2:
        raise ValueError("Expected CPU and memory columns")

    total_values = data.size
    missing_values = int(np.isnan(data).sum())

    missing_rate = missing_values / total_values if total_values else 0.0

    completeness = min(data.shape[0] / expected_points, 1.0)

    return {
        "missing_values": missing_values,
        "missing_rate": round(missing_rate, 5),
        "completeness": round(completeness, 5),
    }
