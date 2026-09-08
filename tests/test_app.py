from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"
    assert data["version"] == "1.0.0"


def test_prediction():
    response = client.post(
        "/predict",
        json={"value": 10}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["input"] == 10
    assert data["prediction"] == 20
