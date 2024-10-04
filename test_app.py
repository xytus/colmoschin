import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    """Unit tests for the Flask application."""

    def setUp(self):
        # Set up a test client for the Flask application
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home(self):
        """Test the home route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Simple Flask App", response.data)
        self.assertIn(b"This application was created by Col Moschin.", response.data)

if __name__ == '__main__':
    unittest.main()
