from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Running successfully"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_summarize_without_api_key():
    response = client.post(
        "/api/v1/summarize",
        json={
            "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
            "length": "short",
            "style": "professional",
        },
    )
    assert response.status_code == 401


def test_summarize_with_invalid_api_key():
    response = client.post(
        "/api/v1/summarize",
        headers={"x-API-Key": "Wrong=api-key"},
        json={
            "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
            "length": "short",
            "style": "professional",
        },
    )
    assert response.status_code == 401
