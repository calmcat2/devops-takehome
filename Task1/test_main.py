from fastapi.testclient import TestClient
from unnitest.mock import patch

with patch("sqlmodel.create_engine") as mock_create_engine:
    mock_create_engine.return_value = None  # Prevent real engine creation
    from .main import app, get_session

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# def test_create_item():
#     response = client.post(
#         "/stores/",
#         headers={"Content-Type": "application/json"},
#         json={"name": "Smith's"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": "1",
#         "name": "Smith's",
#     }