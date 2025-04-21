import pytest
from fastapi.testclient import TestClient
from main import app
from app.database.provider import DatabaseProvider
from app.config.settings import get_settings

import os

os.environ["ENVIRONMENT"] = "test"

def pytest_configure():
    get_settings()

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_age_groups_collection():
    db = DatabaseProvider.get_db()
    db.drop_collection("age_groups")
    yield
    db.drop_collection("age_groups")
