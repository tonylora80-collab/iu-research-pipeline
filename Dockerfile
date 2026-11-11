FROM python:3.11-slim

WORKDIR /app

COPY scripts/ ./scripts/
COPY data/raw_samples.csv ./data/raw_samples.csv

CMD ["python3", "scripts/validate_data.py"]
