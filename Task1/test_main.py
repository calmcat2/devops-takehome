from typing import Optional
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlmodel import create_engine, SQLModel, Session, Field
from .main import app

# Create an in-memory SQLite engine for testing
test_engine = create_engine("sqlite:///:memory:", echo=True)

class Store(SQLModel,table=True):
    id: Optional[int]=Field(default=None,primary_key=True)
    name: str

# Initialize database schema for testing
SQLModel.metadata.create_all(test_engine)

# Override session dependency to use test engine
def get_test_session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    # Patch create_engine globally before tests run
    with patch("sqlmodel.create_engine", return_value=test_engine):
        yield

# Apply dependency override for testing
app.dependency_overrides["get_session"] = get_test_session

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
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "name": "Smith's",
    }