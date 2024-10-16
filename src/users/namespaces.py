from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.users.services import *

# Logger configuration
logger = logging.getLogger(__name__)

# Create Namespace for users
users_ns = Namespace('users', description='User related operations', tags=['users'])

# Define models for input/output with Flask-RESTX
signup_model = users_ns.model('SignUp', {
    'firstname': fields.String(required=True, description='First name of the user'),
    'lastname': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

login_model = users_ns.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

response_model = users_ns.model('Response', {
    'status': fields.String(description='Status of the response'),
    'message': fields.String(description='Message of the response')
})

token_response_model = users_ns.clone('TokenResponse', response_model, {
    'tokens': fields.Raw(description='Access and refresh tokens')
})


# User Signup Resource
@users_ns.route('/signup')
class UserSignup(Resource):
    @users_ns.expect(signup_model, validate=True)
    @users_ns.response(201, 'User successfully signed up', token_response_model)
    @users_ns.response(400, 'Validation Error')
    @users_ns.response(409, 'Conflict Error - User already exists')
    def post(self):
        """
        Sign up a new user
        """
        data = request.get_json()
        role = data.get('role', 'user')  # Default role is 'user'
        tokens = signup_user(data, role=role)
        return {'status': "success", "message": "User Sign up Successful", "tokens": tokens}, 201


# User Login Resource
@users_ns.route('/login')
class UserLogin(Resource):
    @users_ns.expect(login_model, validate=True)
    @users_ns.response(200, 'User successfully logged in', token_response_model)
    @users_ns.response(400, 'Validation Error')
    @users_ns.response(404, 'User not found')
    def post(self):
        """
        Log in an existing user
        """
        data = request.get_json()
        tokens = login_user(data)
        return {'status': "success", "message": "User Login Successful", "tokens": tokens}, 200


# User Logout Resource
@users_ns.route('/logout')
class UserLogout(Resource):
    @jwt_required()
    @users_ns.response(200, 'Successfully logged out', response_model)
    @users_ns.response(401, 'Unauthorized')
    def post(self):
        """
        Log out the current user
        """
        jti = get_jwt_identity()
        # Here you should call a service to revoke the token
        return {'status': 'success', 'message': 'Successfully logged out'}, 200
