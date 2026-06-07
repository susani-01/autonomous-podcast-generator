from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from podcast_app.main import app

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_root_has_endpoints():
    response = client.get("/")
    data = response.json()
    assert "endpoints" in data


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_status_healthy():
    response = client.get("/health")
    assert response.json()["status"] == "healthy"


def test_generate_missing_body():
    response = client.post("/generate", json={})
    assert response.status_code == 400


def test_generate_with_text():
    with patch("podcast_app.main.generate_podcast") as mock_task:
        mock_result = MagicMock()
        mock_result.id = "fake-task-id-123"
        mock_task.delay.return_value = mock_result

        response = client.post(
            "/generate", json={"text": "AI is changing the world.", "music": False}
        )

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert data["task_id"] == "fake-task-id-123"
        assert data["status"] == "PENDING"


def test_generate_requires_text_or_url():
    response = client.post("/generate", json={"music": True})
    assert response.status_code == 400


def test_status_pending():
    with patch("podcast_app.main.celery_app") as mock_celery:
        mock_result = MagicMock()
        mock_result.state = "PENDING"
        mock_celery.AsyncResult.return_value = mock_result

        response = client.get("/status/fake-task-id")
        assert response.status_code == 200
        assert response.json()["status"] == "PENDING"


def test_status_success():
    with patch("podcast_app.main.celery_app") as mock_celery:
        mock_result = MagicMock()
        mock_result.state = "SUCCESS"
        mock_result.result = {
            "job_id": "abc123",
            "total_lines": 16,
            "podcast_path": "podcast_app/outputs/abc123/podcast.mp3",
            "script": [],
        }
        mock_celery.AsyncResult.return_value = mock_result

        response = client.get("/status/fake-task-id")
        assert response.status_code == 200
        assert response.json()["status"] == "SUCCESS"
