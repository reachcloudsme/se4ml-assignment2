import numpy as np
from model.inference import calculate_anomaly_score
from model.training import train_calibrator

from quality.model_quality import measure_model_quality
from quality.time_rcd_experiment import generate_dataset


def evaluate_pipeline():
    train_windows, train_labels = generate_dataset(100)
    test_windows, test_labels = generate_dataset(200)

    print("Generating actual Time-RCD scores...")

    train_scores = np.array(
        [calculate_anomaly_score(window) for window in train_windows]
    )
    test_scores = np.array([calculate_anomaly_score(window) for window in test_windows])

    calibrator = train_calibrator(train_scores, train_labels)

    predictions = calibrator.predict(test_scores.reshape(-1, 1))
    probabilities = calibrator.predict_proba(test_scores.reshape(-1, 1))[:, 1]

    results = measure_model_quality(test_labels, predictions)
    results["true_negatives"] = int(((test_labels == 0) & (predictions == 0)).sum())

    print("Training windows:", len(train_windows))
    print("Evaluation windows:", len(test_windows))
    print("Training score range:", train_scores.min(), train_scores.max())
    print("Evaluation score range:", test_scores.min(), test_scores.max())
    print("Actual labels:", test_labels.tolist())
    print("Predicted labels:", predictions.tolist())
    print("Calibrated probabilities:", np.round(probabilities, 4).tolist())
    print("Model quality:", results)

    return results


if __name__ == "__main__":
    evaluate_pipeline()
