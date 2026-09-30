# AI-Powered Chatbot

A beginner-friendly customer-support chatbot built with Python, FastAPI, SQLite, and a responsive web interface.

## Features

- FastAPI REST backend
- FAQ / intent detection
- Confidence score
- Conversation logging in SQLite
- Recent conversation API
- Responsive browser chat UI
- Automated API tests
- Ready for GitHub and Render deployment

## Project Structure

```text
AI-Powered-Chatbot/
├── backend/
│   ├── main.py
│   ├── chatbot.py
│   └── database.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── data/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Run Locally

### 1. Create environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Start server

```bash
uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Test

```bash
pytest
```

## Deployment

The application can be deployed on a Python web service such as Render using:

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

## Future Improvements

- Transformer-based semantic intent classification
- User authentication
- Admin dashboard
- Better conversation context
- PostgreSQL for production
- Docker
- Cloud deployment
