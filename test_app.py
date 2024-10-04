import pytest
from app import app

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Our Simple Flask Web Application" in response.data
    assert b"Created by: [Your Group Name]" in response.data
