import numpy as np

from quality.data_quality import measure_data_quality


def evaluate_data_quality():
    # Representative synthetic CPU/memory telemetry, not live Mimir data.
    window = np.column_stack(
        [
            np.linspace(0.1, 0.5, 21),
            np.linspace(100, 200, 21),
        ]
    )
    window[5, 0] = np.nan

    return measure_data_quality(window)


if __name__ == "__main__":
    print(evaluate_data_quality())
