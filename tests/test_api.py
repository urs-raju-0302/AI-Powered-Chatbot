from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat():
    response = client.post("/api/chat", json={"message": "I forgot my password"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "password_reset"
    assert "password" in data["response"].lower()
