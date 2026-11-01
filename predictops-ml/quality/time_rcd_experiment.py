import numpy as np
from model.inference import calculate_anomaly_score


def make_window(pattern, seed=42):
    rng = np.random.default_rng(seed)
    cpu = 0.2 + rng.normal(0, 0.01, 21)
    memory = 100_000_000 + rng.normal(0, 1_000_000, 21)

    if pattern == "cpu_spike":
        cpu[-5:] += 0.6
    elif pattern == "memory_spike":
        memory[-5:] += 100_000_000
    elif pattern != "normal":
        raise ValueError("Unknown telemetry pattern")

    return np.column_stack([cpu, memory])


if __name__ == "__main__":
    for pattern in ("normal", "cpu_spike", "memory_spike"):
        score = calculate_anomaly_score(make_window(pattern))
        print(f"{pattern}: Time-RCD score = {score:.5f}")


def generate_dataset(start_seed, samples_per_pattern=6):
    windows = []
    labels = []

    for pattern, label in (
        ("normal", 0),
        ("cpu_spike", 1),
        ("memory_spike", 1),
    ):
        for seed in range(start_seed, start_seed + samples_per_pattern):
            windows.append(make_window(pattern, seed=seed))
            labels.append(label)

    return windows, np.asarray(labels, dtype=int)
