# PredictOps — ML-Based Anomaly Detection

**Course:** AIMLZG546 — Software Engineering for Machine Learning
**Assignment:** II — Implementation and Quality Assurance
**Group:** 56

## Overview

PredictOps monitors banking microservices using CPU and memory telemetry collected through Prometheus and Grafana Mimir.

A pretrained Time-RCD model generates anomaly scores. FastAPI exposes scoring and monitoring endpoints.

Assignment II focuses on modular design, API reliability, logging, automated testing, model training, inference validation and quality evaluation.

## Architecture

Production monitoring:

Banking Microservices → Prometheus/Mimir → Time-RCD → FastAPI Metrics → Prometheus Alerts → Alertmanager

Experimental evaluation:

Synthetic Telemetry → Time-RCD Scores → Trained Logistic Regression Calibrator → Predictions → Precision and Recall

The experimental calibrator does not control production alerts.

## Project Structure

| File or directory | Purpose |
|---|---|
| `predictops-ml/app.py` | FastAPI endpoints and scoring |
| `predictops-ml/api_schemas.py` | Pydantic response schemas |
| `predictops-ml/data/mimir.py` | Metrics retrieval and logging |
| `predictops-ml/model/inference.py` | Time-RCD inference and validation |
| `predictops-ml/model/training.py` | Logistic regression calibrator training |
| `predictops-ml/quality/data_quality.py` | Missingness and completeness |
| `predictops-ml/quality/model_quality.py` | Precision, recall and confusion counts |
| `predictops-ml/quality/data_quality_evaluation.py` | Synthetic data-quality demonstration |
| `predictops-ml/quality/evaluation.py` | Synthetic calibrator-only evaluation |
| `predictops-ml/quality/time_rcd_experiment.py` | Synthetic telemetry generation |
| `predictops-ml/quality/pipeline_evaluation.py` | Actual Time-RCD and calibrator evaluation |
| `predictops-ml/tests/` | Automated pytest tests |
| `predictops-ml/Dockerfile` | Containerised inference API |
| `evidence/` | Historical code and refactoring comparison |

## REST API

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Health status |
| `/metrics` | GET | Prometheus-compatible metrics |
| `/score` | POST | Score all configured services |
| `/score/{service}` | POST | Score a selected service |

Single-service API tests cover successful HTTP 200 scoring, unknown-service 404, upstream-data errors 502, unavailable metrics 503 and inference failures 500.

## Automated Testing

Run from the repository root after installing dependencies:

    python -m pytest predictops-ml/tests/ -v

**Latest verified result: 28 tests passed.**

Tests include API behaviour, Mimir retrieval, missing-data warnings, data validation, inference validation, model training and quality evaluation.

## Code Quality and Security

    python -m ruff check predictops-ml/
    python -m black --check predictops-ml/
    python -m bandit -r predictops-ml/ -x predictops-ml/tests/

Ruff and Black checks passed. Bandit reported zero findings in 386 scanned lines in the earlier final evaluation scan. This does not guarantee complete security.

## Model Training

The experimental logistic regression calibrator is trained on labelled anomaly scores.

In the small-batch synthetic training test:

- Initial binary cross-entropy: **0.69315**
- Trained binary cross-entropy: **0.00103**

The pretrained Time-RCD model remains frozen.

## End-to-End Model Evaluation

Run:

    PYTHONPATH=predictops-ml python -m quality.pipeline_evaluation

The experiment uses actual pretrained Time-RCD inference on reproducible synthetic CPU and memory windows, followed by calibration and held-out evaluation.

| Measurement | Result |
|---|---:|
| Training windows | 18 |
| Evaluation windows | 18 |
| Precision | 70.59% |
| Recall | 100% |
| Accuracy | 72.22% |
| True positives | 12 |
| True negatives | 1 |
| False positives | 5 |
| False negatives | 0 |
| False-positive rate | 83.33% |

The high false-positive rate indicates limited discrimination of normal windows. An always-anomaly baseline would achieve 66.67% precision and 100% recall on this class distribution.

These results are from **synthetic telemetry with controlled changes**, not labelled production banking incidents.

## Data Quality

Run:

    PYTHONPATH=predictops-ml python -m quality.data_quality_evaluation

Results from the synthetic telemetry sample:

- Missing values: 1 of 42
- Missing-value rate: 2.381%
- Row-count completeness: 21/21 = 100%

Row-count completeness does not independently validate timestamp uniqueness or sampling alignment.

## Research vs Production Code

The historical Assignment I implementation is available at commit `cac4709`.

See:

- `evidence/assignment1_app.py.txt`
- `evidence/research_vs_production.diff`

The original implementation combined telemetry retrieval, inference and API logic in one file. Assignment II separates modules and adds automated tests, validation, structured responses and logging.

## Deployment Scope

The earlier threshold-based PredictOps API was deployed and verified on AWS EKS using Docker and Kubernetes.

The newer experimental calibration workflow was evaluated locally. It has not been deployed into production or connected to production alert decisions.

The Dockerfile is intended for the inference API, not the full experimental training environment.

## Installation and Reproducibility

Use Python 3.12 for the local experimental workflow. From the repository root:

    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r predictops-ml/requirements.txt -r predictops-ml/requirements-dev.txt
    python -m pip install torch scipy huggingface-hub jaxtyping einops
    python -m pip install --no-deps "git+https://github.com/thu-sail-lab/Time-RCD.git"

The pretrained model may download additional weights when first loaded. CPU execution is supported.

## Production Experimentation and Security

A future shadow deployment could compare candidate anomaly predictions with the existing threshold-based service before changing alert decisions.

The Docker/Kubernetes application uses a non-root user, disables privilege escalation and drops Linux capabilities.

## Repository

**GitHub:** https://github.com/reachcloudsme/se4ml-assignment2

**Assignment II branch:** `assignment2-improvements`

**Last published evaluation commit:** `7d6faf3` (subsequent improvements may change this).

## Attribution

The banking microservices workload is separate from the PredictOps ML monitoring and evaluation code. Attribution to its original project should be verified against the actual source repository before submission.
