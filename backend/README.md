# Phishing Email Detection Model - Backend

This backend provides a FastAPI service with an ML pipeline to classify emails as `phishing` or `safe`.

Quick setup

1. Create virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Train model (produces `model.joblib` and `metrics.json`):

```powershell
python train.py
```

3. Run API:

```powershell
uvicorn app.main:app --reload --port 8000
```

Endpoints

- `POST /analyze` - analyze email text (JSON: `{ "email": "..." }`)
- `GET /metrics` - model metrics and confusion matrix data
 - `POST /report` - return a PDF threat report for submitted email (JSON: `{ "email": "..." }`)

Docker

Build and run with docker-compose:

```powershell
docker-compose up --build
```

Security: educational and defensive use only.
