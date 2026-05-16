# ujmikamiapp

Personal portfolio site — React frontend + Django REST API.

## Stack

- **Frontend:** React 19 + TypeScript
- **Backend:** Django 6 + Django REST Framework + SQLite
- **Deployment:** Docker Compose (backend on `:8000`, frontend on `:3000`)

## Quick Start

### Backend

```bash
cd backend/ujmikamiapp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Migrate + seed
python manage.py migrate
python manage.py seed_ml_models

# Run
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
REACT_APP_API_BASE_URL=http://localhost:8000 npm start
```

Opens on `http://localhost:3000`.

### Docker

```bash
docker compose up --build
```

---

## API Endpoints

### Projects

| Method | Path                     | Description                  |
|--------|--------------------------|------------------------------|
| GET    | `/api/projects/`         | List all portfolio projects  |
| GET    | `/api/projects/<id>/`    | Single project detail        |

Optional query param: `?category=ml` to filter by category.

### ML Models (new)

| Method | Path                      | Description                           |
|--------|---------------------------|---------------------------------------|
| GET    | `/api/ml-models/`         | List all ML model showcase entries    |
| GET    | `/api/ml-models/<id>/`    | Single ML model detail with metrics   |

**Example:**

```bash
curl http://localhost:8000/api/ml-models/
curl http://localhost:8000/api/ml-models/1/
```

Response shape (list):

```json
[
  {
    "id": 1,
    "title": "Chatbot Arena — LLM Preference Classification",
    "description": "…",
    "category": "nlp",
    "category_display": "NLP & Text",
    "architecture": "DistilBERT (distilbert-base-uncased)",
    "framework": "PyTorch + HuggingFace Transformers",
    "competition_name": "LLM Classification Finetuning (Chatbot Arena)",
    "competition_url": "https://…",
    "dataset_description": "…",
    "metrics": { "log_loss": 1.04331 },
    "rank": "112 / 257",
    "score": "1.04331",
    "image": null,
    "links": [
      { "id": 1, "label": "Competition Page", "url": "https://…" }
    ],
    "order": 1,
    "created_at": "2026-05-16T…"
  }
]
```

---

## Seeding ML Models

```bash
cd backend/ujmikamiapp
python manage.py seed_ml_models          # replace all entries
python manage.py seed_ml_models --clear-only  # delete all entries only
```

The seed command populates 3 entries:

| # | Project                                    | Domain      | Model                            |
|---|--------------------------------------------|-------------|----------------------------------|
| 1 | Chatbot Arena (LLM preference prediction)  | NLP         | DistilBERT + TF-IDF baseline     |
| 2 | Disaster Tweets classification             | NLP         | DeBERTa-v3 + XGBoost ensemble    |
| 3 | Fashion-MNIST (AI-Biz2026)                 | CV          | ResNet CNN + specialist ensemble |

Each entry includes competition links, notebook URLs, metrics, and leaderboard rank.

---

## Testing

```bash
cd backend/ujmikamiapp
python manage.py test ml_models
```

Tests cover both list and detail API endpoints.
