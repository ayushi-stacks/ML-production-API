from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction():
    payload = {
        "lag_1": 85.4,
        "lag_2": 91.2,
        "lag_3": 78.6,
        "lag_7": 102.3,
        "rolling_3": 85.1,
        "rolling_7": 88.4,
        "rolling_14": 92.7,
        "day_of_week": 2,
        "day_of_year": 265,
        "week_of_year": 39
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "predicted_pm25" in result
    assert "unit" in result
    assert result["unit"] == "µg/m³"
    assert isinstance(result["predicted_pm25"], float)