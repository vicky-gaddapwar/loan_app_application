# tests/test_user.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.database.db import get_db, SessionLocal

client = TestClient(app)

# Dependency override to use a test database
@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test user registration
def test_register(db_session):
    response = client.post("/user/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test user login
def test_login(db_session):
    client.post("/user/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/user/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test submit loan application
def test_submit_loan(db_session):
    response = client.post("/user/login", json={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]
    response = client.post(
        "/user/submit-loan",
        headers={"Authorization": f"Bearer {token}"},
        json={"loan_amount": 10000, "loan_purpose": "Home Renovation", "duration": 12, "contact_details": "1234567890"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Loan application submitted"
