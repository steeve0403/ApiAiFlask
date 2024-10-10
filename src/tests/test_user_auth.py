import unittest
from flask import json
from src import app, db
from src.models.user_model import User
from flask_jwt_extended import create_access_token

class UserAuthTests(unittest.TestCase):
    """
    Test suite for user authentication including signup, login, logout, and API key generation.
    """

    def setUp(self):
        """
        Setup a temporary database and initialize the Flask test client.
        """
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        db.init_app(self.app)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Drop the temporary database after the tests.
        """
        with self.app.app_context():
            db.drop_all()

    def test_user_signup(self):
        """
        Test for user signup.
        """
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/auth/signup', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User Sign up Successful', response.json['message'])

    def test_user_login(self):
        """
        Test for user login.
        """
        with self.app.app_context():
            hashed_password = User.generate_password_hash('password123')
            user = User(firstname="John", lastname="Doe", email="john.doe@example.com", password=hashed_password)
            db.session.add(user)
            db.session.commit()

        payload = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/auth/signin', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User Login Successful', response.json['message'])

    def test_user_logout(self):
        """
        Test for user logout.
        """
        with self.app.app_context():
            access_token = create_access_token(identity={'user_id': 1, 'role': 'user'})
            headers = {'Authorization': f'Bearer {access_token}'}

        response = self.client.post('/api/auth/logout', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully logged out', response.json['message'])

    def test_generate_api_key(self):
        """
        Test for API key generation.
        """
        with self.app.app_context():
            user = User(firstname="Jane", lastname="Doe", email="jane.doe@example.com", password=User.generate_password_hash('password456'))
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity={'user_id': user.id, 'role': 'user'})
            headers = {'Authorization': f'Bearer {access_token}'}

        response = self.client.post('/api/auth/generate-api-key', headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('api-key', response.json)

if __name__ == "__main__":
    unittest.main()
