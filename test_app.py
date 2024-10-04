import pytest
from app import app

@pytest.fixture
def client():
    # Setup the test client for the Flask app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Simple Flask App" in response.data
    assert b"This application was created by Col Moschin." in response.data
