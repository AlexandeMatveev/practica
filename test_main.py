from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_and_get_user():
    response = client.post("/users", json={"name": "Мария", "age": 28})
    assert response.status_code == 201
    assert response.json()["name"] == "Мария"

    response = client.get("/users")
    assert len(response.json()) >= 1