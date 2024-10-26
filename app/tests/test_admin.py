# tests/test_admin.py

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

# Test admin approve/reject loan application
def test_admin_approve_loan(db_session):
    # Create an admin user for testing
    client.post("/user/register", json={"username": "adminuser", "password": "adminpass", "role": "admin"})
    # Login as admin
    response = client.post("/user/login", json={"username": "adminuser", "password": "adminpass"})
    token = response.json()["access_token"]
    
    # Create a loan application
    client.post("/user/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/user/login", json={"username": "testuser", "password": "testpass"})
    user_token = response.json()["access_token"]
    client.post(
        "/user/submit-loan",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"loan_amount": 10000, "loan_purpose": "Home Renovation", "duration": 12, "contact_details": "1234567890"}
    )
    
    # Get the application id from the submitted loan
    loan_response = client.get("/user/view-status/1", headers={"Authorization": f"Bearer {user_token}"})
    application_id = loan_response.json()["application_id"]
    
    # Admin approves the loan application
    response = client.put(
        f"/admin/applications/{application_id}/status?status=approved",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
