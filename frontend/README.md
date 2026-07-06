# Portfolio: Software Engineering & Machine Learning

Vitajte na mojom osobnom portfóliu. Tento web slúži ako prezentácia mojich projektov v oblasti softvérového inžinierstva a strojového učenia, ktoré som vyvinul ako súčasť mojej cesty za pokročilým vývojom backend systémov a modelov.

Aplikáciu si môžete pozrieť na adrese: https://zealous-bay-04c9a6603.7.azurestaticapps.net/.

## O projekte

Táto platforma spája moderný frontend s robustným backendom. Frontend je postavený na React 19 v kombinácii s TypeScriptom, zatiaľ čo backend využíva Django 6 a Django REST Framework na efektívne spravovanie dát a API komunikáciu.

## Technologický stack

Frontend: React 19, TypeScript
Backend: Django 6, Django REST Framework, SQLite
Nasadenie: Docker Compose

## Inštalácia a spustenie

Pre spustenie lokálnej verzie projektu postupujte nasledovne:

### Backend

Prejdite do zložky backendu a pripravte si virtuálne prostredie:
cd backend/ujmikamiapp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

Následne spustite migráciu databázy a naplňte ju dátami:
python manage.py migrate
python manage.py seed_ml_models
python manage.py runserver

### Frontend

V zložke frontend nainštalujte závislosti a spustite vývojový server:
cd frontend
npm install
REACT_APP_API_BASE_URL=http://localhost:8000 npm start

Pre komplexné spustenie pomocou Dockeru môžete použiť príkaz:
docker compose up --build

## Prehľad API

Projekt obsahuje REST API rozhranie pre správu projektov a modelov strojového učenia.

### Projekty

GET /api/projects/: Zoznam všetkých projektov
GET /api/projects/<id>/: Detail konkrétneho projektu

### Strojové učenie

GET /api/ml-models/: Prehľad mojich projektov v oblasti ML
GET /api/ml-models/<id>/: Detail modelu vrátane metrík a leaderboardu

## ML Modely

Integrovaná podpora pre seeding modelov umožňuje jednoduchú správu obsahu. V súčasnosti projekt obsahuje:
Chatbot Arena (predikcia preferencií LLM)
Klasifikácia tweetov o katastrofách
Fashion-MNIST (úspešný projekt v súťaži AI-Biz2026)

Pre spustenie testov backendovej časti použite príkaz python manage.py test ml_models v zložke backendu.