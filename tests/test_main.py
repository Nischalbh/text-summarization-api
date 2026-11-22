from fastapi.testclient import TestClient
from app.main import app
from app.core.security import verify_api_key
from app.core.rate_limiter import rate_limit
from unittest.mock import patch, AsyncMock
from google.genai import errors as genai_errors

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


def test_summarize_with_short_text():
    app.dependency_overrides[verify_api_key] = lambda: "test-api-key"

    try:
        response = client.post(
            "/api/v1/summarize",
            json={
                "text": "Too short",
                "length": "short",
                "style": "professional",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()


def test_summarize_with_invalid_length():
    app.dependency_overrides[rate_limit] = lambda: None

    try:
        response = client.post(
            "/api/v1/summarize",
            json={
                "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
                "length": "extra-long",
                "style": "professional",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.pop(rate_limit, None)


def test_summarize_with_invalid_style():
    app.dependency_overrides[rate_limit] = lambda: None

    try:
        response = client.post(
            "/api/v1/summarize",
            json={
                "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
                "length": "short",
                "style": "invalid-style",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.pop(rate_limit, None)


def test_summarize_success():
    app.dependency_overrides[rate_limit] = lambda: None

    mock_result = "AI improves efficiency through automation."

    try:
        with patch(
            "app.main.summarize_long_text",
            return_value=mock_result,
        ):
            response = client.post(
                "/api/v1/summarize",
                headers={"x-API-Key": "your-real-client-api-key"},
                json={
                    "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
                    "length": "short",
                    "style": "professional",
                },
            )

        assert response.status_code == 200
        assert response.json()["summary"] == mock_result
        assert response.json()["chunks_processed"] == 1

    finally:
        app.dependency_overrides.pop(rate_limit, None)


def test_summarize_gemini_error():
    app.dependency_overrides[rate_limit] = lambda: None

    try:
        with patch(
            "app.main.summarize_long_text",
            side_effect=genai_errors.APIError(
                503,
                {"message": "Gemini service unavailable"},
            ),
        ):
            response = client.post(
                "/api/v1/summarize",
                headers={"x-API-Key": "your-real-client-api-key"},
                json={
                    "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
                    "length": "short",
                    "style": "professional",
                },
            )

        assert response.status_code == 502

    finally:
        app.dependency_overrides.pop(rate_limit, None)


def test_summarize_unexpected_error():
    app.dependency_overrides[rate_limit] = lambda: None

    try:
        with patch(
            "app.main.summarize_long_text",
            side_effect=Exception("Unexpected test error"),
        ):
            response = client.post(
                "/api/v1/summarize",
                headers={"x-API-Key": "your-real-client-api-key"},
                json={
                    "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
                    "length": "short",
                    "style": "professional",
                },
            )

        assert response.status_code == 500

    finally:
        app.dependency_overrides.pop(rate_limit, None)


def test_rate_limit_exceeded():
    with patch(
        "app.core.rate_limiter.redis_client.eval",
        new_callable=AsyncMock,
        return_value=11,
    ):
        response = client.post(
            "/api/v1/summarize",
            headers={"x-API-Key": "Ac0U5qyLcGNtOTgIcCyxIlip0OceU_kg-_RFUfkTNg8"},
            json={
                "text": "This is a sample text that contains more than fifty characters for testing the summarization API.",
                "length": "short",
                "style": "professional",
            },
        )

    assert response.status_code == 429
