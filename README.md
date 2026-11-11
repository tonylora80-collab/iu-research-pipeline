# Secure Research Data Pipeline

An automated, containerized clinical research data validation pipeline and Infrastructure-as-Code (IaC) blueprint designed for HIPAA-compliant cloud environments.

## Architecture & Key Components

* **PHI De-identification & QC (`scripts/validate_data.py`):** Python ETL script that validates incoming genomic sample records, rejects incomplete or failed quality-control entries, and strips Protected Health Information (PHI) prior to cloud ingestion.
* **Containerized Runtime (`Dockerfile`):** Lightweight `python:3.11-slim` container ensuring reproducible execution across local workstations, on-premises HPC clusters, and AWS cloud compute nodes.
* **Cloud Infrastructure as Code (`infrastructure/main.tf`):** Terraform configuration provisioning an AWS S3 research archive with enforced AES-256 server-side encryption and strict zero-trust public access blocks.
* **Automated CI/CD Pipeline (`.github/workflows/ci.yml`):** GitHub Actions workflow that automatically validates Python data processing, builds and tests the Docker container, and verifies Terraform syntax on every commit.

## Quick Start

### Run Locally with Python
```bash
python3 scripts/validate_data.py
```

### Run via Docker
```bash
docker build -t iu-research-validator .
docker run --rm iu-research-validator
```

### Validate Cloud Infrastructure
```bash
cd infrastructure
terraform init -backend=false
terraform validate
```
