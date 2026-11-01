from fastapi.testclient import TestClient

from app import app


class TestHealthEndpoint:
    def test_answers_ok_when_the_application_is_running(self) -> None:
        response = TestClient(app).get("/health/")

        assert response.status_code == 200
        assert response.json() == "OK"
