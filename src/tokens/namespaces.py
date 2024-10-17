from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from src.tokens.services import create_jwt_token, refresh_access_token, revoke_jwt_token, get_current_user
from src.exceptions import ValidationError

# Logger configuration
import logging

logger = logging.getLogger(__name__)

# Define the Namespace
token_ns = Namespace('tokens', description='Operations related to JWT tokens', tags=['tokens'])

# Define models for input/output with Flask-Restx
login_model = token_ns.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})

token_response_model = token_ns.model('TokenResponse', {
    'access_token': fields.String(description='Access token'),
    'refresh_token': fields.String(description='Refresh token')
})

token_refresh_model = token_ns.model('TokenRefreshResponse', {
    'access_token': fields.String(description='New access token')
})

revoke_model = token_ns.model('Revoke', {
    'token_jti': fields.String(required=True, description='JTI of the token to revoke')
})


# Define the resources (endpoints)

@token_ns.route('/login')
class TokenLogin(Resource):
    @token_ns.expect(login_model, validate=True)
    @token_ns.response(200, 'Successfully logged in', token_response_model)
    @token_ns.response(400, 'Invalid input data')
    @token_ns.response(401, 'Unauthorized')
    def post(self):
        """
        Log in a user and return access and refresh tokens.
        """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise ValidationError("Email and password are required.")

        # Here you can call the service to authenticate and return tokens
        tokens = create_jwt_token(user_id=1, role='user')  # This should be replaced by actual user logic
        return jsonify(tokens), 200


@token_ns.route('/refresh')
class TokenRefresh(Resource):
    @token_ns.response(200, 'Successfully refreshed token', token_refresh_model)
    @token_ns.response(401, 'Unauthorized')
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh the access token using a valid refresh token.
        """
        return refresh_access_token()


@token_ns.route('/revoke')
class TokenRevoke(Resource):
    @token_ns.expect(revoke_model, validate=True)
    @token_ns.response(200, 'Token successfully revoked')
    @token_ns.response(400, 'Invalid input')
    @jwt_required()
    def post(self):
        """
        Revoke a JWT token by its JTI.
        """
        data = request.get_json()
        token_jti = data.get('token_jti')
        if not token_jti:
            raise ValidationError("Token JTI is required.")

        revoke_jwt_token(token_jti)
        return jsonify({"message": "Token successfully revoked"}), 200


@token_ns.route('/user')
class TokenUser(Resource):
    @token_ns.response(200, 'Current user information retrieved')
    @token_ns.response(401, 'Unauthorized')
    @jwt_required()
    def get(self):
        """
        Get the current user based on the JWT token.
        """
        return get_current_user()
