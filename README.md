# Airflow ML Pipeline - Local Development Setup

A local development environment for running Machine Learning pipelines with Apache Airflow using Docker containers. This project orchestrates ML workflows including data loading, preprocessing, training, evaluation, and deployment.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Using the Pipeline](#using-the-pipeline)
- [Development Workflow](#development-workflow)

---

## 🎯 Overview

**Tech Stack:**
- **Apache Airflow 3.1.5** - Workflow orchestration
- **Docker & Docker Compose** - Containerization
- **Python 3.11+** - ML development
- **scikit-learn** - Machine learning
- **UV** - Fast Python package management

**Pipeline Tasks:**
1. Load data from S3/object storage
2. Preprocess data
3. Train model with MLflow tracking
4. Evaluate model performance
5. Run custom Docker container
6. Deploy model

---

## ✅ Prerequisites

- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Python 3.11+**
- Docker permissions: `sudo usermod -aG docker $USER` (then log out/in)

---

## � Quick Start

### 1. Build and Push ML Docker Image

```bash
# Build the image
docker build -t pauloyuncha/ml-base:latest .

# (Optional) Push to Docker Hub
docker login
docker push pauloyuncha/ml-base:latest
```

### 2. Setup Docker Permissions

```bash
# Check your docker group GID
getent group docker

# Update docker-compose.yaml user line if needed: "50000:YOUR_DOCKER_GID"
```

### 3. Start Airflow

```bash
# Create required directories
mkdir -p dags logs plugins config
chmod -R 777 logs

# Start Airflow
docker compose up -d

# Wait ~60 seconds for initialization
docker compose logs -f airflow-standalone
```

### 4. Access Airflow UI

- **URL:** http://localhost:8080
- **Username:** `admin`
- **Password:** `airflow` #or output random created password


### 5. Run the Pipeline

1. Enable the DAG by toggling the switch next to `example_ml_pipeline`
2. Click the "Play" button (▶️) and select "Trigger DAG"
3. Monitor execution in the graph view
4. Click on tasks to view logs

---

## 🎮 Using the Pipeline

### Example Pipeline Task Overview based on Dags

| Task | Description |
|------|-------------|
| `load_data` | Loads data from S3 using Airflow S3Hook |
| `preprocess_data` | Preprocesses and transforms data |
| `train_model` | Trains ML model with MLflow tracking |
| `evaluate_model` | Evaluates model performance |
| `run_ml_base_container` | Runs custom Docker container with training script |
| `deploy_model` | Deploys model to production |


---

## 🔧 Development Workflow

### Creating a New DAG

```bash
# Create new DAG file
touch dags/k8s_pipeline.py
```

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def my_task():
    print("Hello from my custom task!")

with DAG(
    'k8s_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id='my_task',
        python_callable=my_task,
    )
```

Airflow auto-detects new DAGs every 30 seconds.

### Modifying ML Training Code

```bash
# 1. Edit your training script
vim ml-base/train.py

# 2. Rebuild and push Docker image
docker build -t pauloyuncha/ml-base:latest .
docker push pauloyuncha/ml-base:latest

# 3. Re-run DAG in Airflow UI
```

### Adding Python Dependencies

```bash
# 1. Edit pyproject.toml
# Add new package to dependencies list

# 2. Update lock file
uv lock

# 3. Rebuild Docker image
docker build -t pauloyuncha/ml-base:latest .
docker push pauloyuncha/ml-base:latest
```

### Configuring S3/Object Storage

In Airflow UI: **Admin → Connections → Create**

- **Connection ID:** `s3_default`
- **Connection Type:** `Amazon Web Services`
- **AWS Access Key ID:** `your_access_key`
- **AWS Secret Access Key:** `your_secret_key`
- **Extra:** `{"endpoint_url": "https://your-endpoint.com"}` (for DigitalOcean Spaces)

### Setting Up MLflow Tracking

Add to `docker-compose.yaml`:

```yaml
environment:
  - MLFLOW_TRACKING_URI=http://your-mlflow-server:5000
  - MLFLOW_EXPERIMENT_NAME=breast-cancer-detection
```

Then restart:
```bash
docker compose down
docker compose up -d
```

---

## 📚 Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [UV Package Manager](https://github.com/astral-sh/uv)

---

## 🎉 Quick Commands

```bash
# Build and push ML image
docker build -t pauloyuncha/ml-base:latest .
docker push pauloyuncha/ml-base:latest

# Start Airflow
docker compose up -d

# View logs
docker compose logs -f airflow-standalone

# Stop Airflow
docker compose down
```

---

**Happy ML Pipeline Orchestration! 🚀**

