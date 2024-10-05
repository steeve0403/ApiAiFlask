from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask import jsonify
import jwt
import os

from src.models.token_model import RevokedToken

# Initialize the JWTManager
jwt = JWTManager()

# Secret key for signing JWTs (stored in environment variables for security)
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')


def create_jwt_token(user_id, role, expires_in=24):
    """
    Generate a JWT token with a configurable expiration time.
    The token will also include the user's role for managing future authorizations.

    :param user_id: ID of the user.
    :param role: Role of the user (admin, user, etc.).
    :param expires_in: Lifetime of the token (in hours).
    :return: JWT Token.
    """
    try:
        # Generate the token with user identity and role
        access_token = create_access_token(
            identity={'user_id': user_id, 'role': role},
            expires_delta=timedelta(hours=expires_in)
        )
        refresh_token = create_access_token(identity=user_id)
        return {'access_token': access_token, 'refresh_token': refresh_token}
    except Exception as e:
        return jsonify({'status': 'failed', 'message': 'Error generating token', 'error': str(e)}), 500


def decode_jwt_token(token):
    """
    Decode a JWT token and verify if it's valid or expired.

    :param token: JWT Token to verify.
    :return: Decoded content of the token or error message.
    """
    try:
        decoded_token = decode_token(token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'failed', 'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'failed', 'message': 'Token is invalid'}), 401


# JWT error management for specific scenarios

@jwt_required(refresh=True)
def refresh_access_token():
    """
    Endpoint to refresh the access token using a valid refresh token.
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_access_token}), 200


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    """ Handle errors when the JWT has expired. """
    token_type = expired_token['type']
    return jsonify({
        'status': 'failed',
        'message': f"Your {token_type} token has expired. Please log in again."
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(invalid_token):
    """ Handle errors when a JWT is invalid. """
    return jsonify({
        'status': 'failed',
        'message': "The token is invalid or has been tampered with."
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(callback):
    """ Handle errors when a JWT is missing from the request. """
    return jsonify({
        'status': 'failed',
        'message': "JWT token is missing. Access denied."
    }), 401


@jwt_required()
def get_current_user():
    """
    Retrieve the current user based on the JWT token.
    The identity fetched is the user ID.

    :return: User's ID.
    """
    try:
        current_user_id = get_jwt_identity()
        return current_user_id
    except Exception as e:
        return jsonify({'status': 'failed', 'message': 'Error fetching user', 'error': str(e)}), 500


# Optional: Token revocation management

revoked_tokens = set()  # In-memory store for revoked tokens (can be moved to a database)


def revoke_jwt_token(token_jti):
    """
    Revoke a JWT token by storing its JTI (JWT ID) in the revoked tokens table.
    """
    revoked_token = RevokedToken(jti=token_jti)
    revoked_token.add()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Check if a JWT token has been revoked by querying the revoked tokens table.
    """
    jti = jwt_payload['jti']  # Unique identifier for the JWT token
    return RevokedToken.is_token_revoked(jti)
