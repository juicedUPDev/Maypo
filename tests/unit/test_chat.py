"""Unit tests for chat router."""
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend directory to sys.path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app import app

client = TestClient(app)


def test_create_context_cache():
    response = client.post(
        "/api/chat/cache",
        json={
            "model": "gemini-1.5-pro",
            "contents": ["System instructions and context docs"],
            "ttl_minutes": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cached"
    assert "cache_id" in data


def test_stream_multimodal_chat():
    response = client.post(
        "/api/chat/stream",
        json={
            "messages": [
                {
                    "role": "user",
                    "parts": [{"text": "Hello, testing Gemini streaming!"}]
                }
            ],
            "model": "gemini-1.5-flash"
        }
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    assert "data:" in response.text
