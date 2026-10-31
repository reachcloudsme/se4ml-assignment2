# PredictOps — ML-Based Anomaly Detection for Microservices

**Course:** AIMLZG546 — Software Engineering for Machine Learning  
**Assignment:** II — Implementation, Code Quality and Quality Assurance  
**Group:** 56  
**Technology Stack:** Python, FastAPI, Time-RCD, Docker, Kubernetes, AWS EKS, Prometheus, Grafana Mimir and Alertmanager

## 1. Project Overview

PredictOps is an ML-based monitoring system designed to detect unusual behaviour in a microservices application.

We used a banking microservices environment running on AWS EKS and integrated an ML inference service to analyse application metrics.

The main objective of Assignment II was to improve the software engineering quality of our ML application by implementing modular code, error handling, logging, automated testing, code quality checks and deployment security.

## 2. Project Objectives

This assignment focuses on two major objectives:

**Objective 1 — Implementation and Code Sharing**

- Refactor the ML application into separate modules.
- Improve error handling and logging.
- Develop REST APIs for model inference.
- Apply code formatting and linting.
- Demonstrate production-oriented code organisation.

**Objective 2 — Quality Assurance**

- Implement automated testing using pytest.
- Validate ML inference behaviour.
- Implement data and model quality metrics.
- Improve application security.
- Demonstrate deployment readiness and production monitoring.

## 3. System Architecture

```text
Banking Microservices (AWS EKS)
              |
              v
       Prometheus Metrics
              |
              v
         Grafana Mimir
              |
              v
      PredictOps ML Service
       (Python + FastAPI)
              |
              v
       Time-RCD Inference
              |
              v
        Anomaly Scores
              |
              v
     Prometheus Monitoring
              |
              v
          Alertmanager
              |
              v
       Email Notifications
```

The banking application generates monitoring metrics. PredictOps retrieves those metrics from Mimir, performs anomaly detection using Time-RCD and exposes the results through FastAPI and Prometheus metrics.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API development |
| Time-RCD | ML-based anomaly detection |
| pytest | Automated testing |
| Ruff | Python linting |
| Black | Code formatting |
| Bandit | Python security scanning |
| Docker | Application containerisation |
| AWS ECR | Docker image registry |
| AWS EKS | Kubernetes deployment |
| Prometheus | Metrics and alerting |
| Grafana Mimir | Metrics storage and querying |
| Alertmanager | Alert notification management |
| GitHub | Version control and code sharing |

## 5. Project Structure

The main Assignment II implementation is located inside `predictops-ml/`.

```text
predictops-ml/
├── app.py
├── Dockerfile
├── predictops-ml.yaml
├── data/
│   └── mimir.py
├── model/
│   └── inference.py
├── quality/
│   ├── data_quality.py
│   └── model_quality.py
└── tests/
    ├── test_api.py
    ├── test_mimir.py
    ├── test_inference.py
    ├── test_data_quality.py
    └── test_model_quality.py
```

### Important Files

- **`app.py`** — FastAPI endpoints and application integration.
- **`data/mimir.py`** — Retrieves metrics from Grafana Mimir.
- **`model/inference.py`** — Performs Time-RCD anomaly inference.
- **`quality/data_quality.py`** — Checks data completeness and missing values.
- **`quality/model_quality.py`** — Implements precision and recall calculations.
- **`tests/`** — Contains automated tests for the application.
- **`Dockerfile`** — Builds the ML application container.
- **`predictops-ml.yaml`** — Defines the Kubernetes deployment and service.

## 6. REST API Implementation

The application exposes the following endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Checks application health |
| `/score` | POST | Runs anomaly scoring across monitored services |
| `/score/{service}` | POST | Runs anomaly scoring for a specified service |
| `/metrics` | GET | Exposes Prometheus-compatible metrics |

Example health check:

```bash
curl http://localhost:8000/health
```

Example anomaly detection:

```bash
curl -X POST http://localhost:8000/score
```

## 7. Automated Testing

We used **pytest** to implement automated testing for critical application components.

Testing covers:

- API endpoint behaviour.
- Mimir data retrieval and error handling.
- ML inference output validation.
- Data quality calculations.
- Model quality calculations.

### Run Tests

From the repository root:

```bash
./.venv/bin/python -m pytest predictops-ml/tests/ -v
```

**Verified result: 11 tests passed.**

These tests provide evidence that the tested components behave as expected under the covered scenarios.

## 8. Code Quality and Security Checks

We used multiple tools to improve code quality.

### Ruff — Linting

```bash
ruff check predictops-ml/
```

**Result:** All checks passed.

### Black — Formatting

```bash
./.venv/bin/python -m black --check predictops-ml/
```

**Result:** 13 files unchanged.

### Bandit — Security Scanning

```bash
./.venv/bin/python -m bandit -r predictops-ml/ -x predictops-ml/tests/
```

**Result:** No security issues identified in the scanned application code.

## 9. Data and Model Quality

We implemented the following quality metrics:

| Category | Metric | Purpose |
|---|---|---|
| Data Quality | Missing-value rate | Measures the proportion of missing data |
| Data Quality | Completeness | Measures the proportion of available data |
| Model Quality | Precision | Measures how many predicted positives are correct |
| Model Quality | Recall | Measures how many actual positives are detected |

The precision and recall calculations were validated using sample labels during testing.

**Limitation:** Actual production precision and recall have not been established using a labelled real-world dataset.

## 10. Docker and Kubernetes Deployment

We containerised the ML application and deployed it to an AWS EKS Kubernetes cluster.

The deployment uses an AMD64-compatible Docker image stored in AWS ECR.

**Docker image tag:** `assignment2-amd64`

We also improved container security by:

- Running the application as a non-root user.
- Disabling privilege escalation.
- Dropping all Linux capabilities.

### Check Kubernetes Deployment

```bash
kubectl get deployment predictops-ml -n default
```

**Verified result:**

```text
NAME            READY   UP-TO-DATE   AVAILABLE
predictops-ml   1/1     1            1
```

## 11. Monitoring and Alerting

PredictOps integrates with Prometheus and Alertmanager to monitor anomaly detection results.

The application exposes metrics including:

```text
predictops_anomaly_score
predictops_anomaly_threshold
predictops_is_anomaly
```

We verified anomaly scoring across eight banking services.

During testing, anomaly alerts fired for:

- `api-gateway`
- `ai-service`
- `fraud-service`

Prometheus successfully evaluated these alerts, and Alertmanager received them.

Alertmanager recorded three email notification attempts without recorded failures. This does not independently confirm delivery to the recipient's inbox.

## 12. Production Testing Strategy

For future production releases, we propose using **shadow deployment**.

In this approach, the new version of PredictOps would analyse the same monitoring data as the existing version, without replacing production alert decisions immediately.

We would compare anomaly scores, system performance and false-positive rates before promoting the new version.

This approach can reduce the risk of introducing changes directly into the production monitoring workflow.

## 13. Assignment II Results

| Activity | Result |
|---|---|
| Modular Python application | Implemented |
| REST API | Implemented |
| Logging and error handling | Implemented |
| Automated pytest tests | 11 passed |
| Ruff linting | Passed |
| Black formatting | Passed |
| Bandit security scan | Passed |
| Data quality metrics | Implemented |
| Model quality metric calculations | Implemented and unit tested |
| Docker image | Built and pushed to ECR |
| AWS EKS deployment | 1/1 available |
| Kubernetes security hardening | Verified |
| Live ML anomaly detection | Verified |
| Prometheus alerting | Verified |
| Alertmanager notification attempts | Verified |

### Remaining Validation

A research-versus-production comparison and a specific model-training test require additional evidence for complete coverage of the assignment rubric.

Real-world model accuracy also requires a labelled evaluation dataset.

## 14. Original Application and Attribution

The PredictOps system uses an existing banking microservices application as the monitored workload.

The original banking application's repository should be linked here after confirming its exact source:

**Original banking application:** `Original Banking Application

The banking microservices application is based on the open-source project maintained by Speedscale.

Original repository: https://github.com/speedscale/microsvc`

The PredictOps contribution focuses on ML-based monitoring, anomaly inference, software quality improvements, testing, deployment and alerting.

## 15. Repository and Branch

**Assignment II branch:** `assignment-2`

**Latest verified Assignment II commit:** `380b7b0`

The repository includes the implementation, tests and deployment configuration used for this assignment.

---

**Course:** AIMLZG546 — Software Engineering for Machine Learning  
**Assignment II | Group 56 | BITS Pilani WILP**
