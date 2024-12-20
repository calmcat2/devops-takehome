from typing import Optional
from fastapi.testclient import TestClient
from sqlmodel import  SQLModel, Session
from sqlalchemy import create_engine
from ..main import app, get_engine, get_session

# Create an in-memory SQLite engine for testing
def get_test_engine():
    return create_engine("sqlite:///:memory:")
test_engine = get_test_engine()

# Override session dependency to use test engine
def get_test_session(engine=test_engine):
    print("Using test session.")
    with Session(engine) as session:
        yield session

# Apply dependency override for testing
app.dependency_overrides[get_engine] = get_test_engine
app.dependency_overrides[get_session] = get_test_session

# Initialize database schema for testing
SQLModel.metadata.create_all(test_engine)

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_item():
    response = client.post(
        "/stores/",
        headers={"Content-Type": "application/json"},
        json={"name": "Smith's"},
    )
    print(response.json())
    assert response.status_code == 200
    data=response.json()
    assert "id" in data
    assert data["name"] == "Smith's"
    