from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity, jwt_required
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import timedelta
from flask import jsonify
import os

from src.extensions import jwt
import logging

from src.tokens.models import RevokedToken
from src.users.models import User

# Logger configuration
logger = logging.getLogger(__name__)

# Secret key for signing JWTs (stored in environment variables for security)
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')


def create_jwt_token(user_id, role, expires_in=24):
    """
    Generate an access token and a refresh token for a user.

    :param user_id: ID of the user.
    :param role: Role of the user (admin, user, etc.).
    :param expires_in: Lifetime of the access token (in hours).
    :return: Dictionary containing access and refresh tokens.
    """
    try:
        # Generate access and refresh tokens with appropriate expiration
        access_token = create_access_token(
            identity={'user_id': user_id, 'role': role},
            expires_delta=timedelta(hours=expires_in)
        )
        refresh_token = create_access_token(
            identity=user_id, expires_delta=timedelta(days=7)  # Longer expiration for refresh token
        )
        return {'access_token': access_token, 'refresh_token': refresh_token}
    except Exception as e:
        logger.error(f"Error generating token: {str(e)}")
        raise


def decode_jwt_token(token):
    """
    Decode a JWT token and verify if it's valid or expired.

    :param token: JWT Token to verify.
    :return: Decoded content of the token or error message.
    """
    try:
        decoded_token = decode_token(token)
        return decoded_token
    except ExpiredSignatureError:
        logger.warning("Token has expired")
        return jsonify({'status': 'failed', 'message': 'Token has expired'}), 401
    except InvalidTokenError:
        logger.warning("Invalid token used")
        return jsonify({'status': 'failed', 'message': 'Token is invalid'}), 401


@jwt_required(refresh=True)
def refresh_access_token():
    """
    Endpoint to refresh the access token using a valid refresh token.

    :return: New access token.
    """
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id, expires_delta=timedelta(minutes=15))
        return jsonify({'access_token': new_access_token}), 200
    except Exception as e:
        logger.error(f"Error refreshing access token: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'Error refreshing token', 'error': str(e)}), 500


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    """
    Handle errors when the JWT has expired.

    :param expired_token: Expired token details.
    :return: JSON response indicating token expiration.
    """
    token_type = expired_token['type']
    logger.warning(f"Expired {token_type} token used")
    return jsonify({
        'status': 'failed',
        'message': f"Your {token_type} token has expired. Please log in again."
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(invalid_token):
    """
    Handle errors when a JWT is invalid.

    :param invalid_token: Invalid token details.
    :return: JSON response indicating invalid token.
    """
    logger.warning("Invalid token attempted")
    return jsonify({
        'status': 'failed',
        'message': "The token is invalid or has been tampered with."
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(callback):
    """
    Handle errors when a JWT is missing from the request.

    :param callback: Callback details.
    :return: JSON response indicating missing token.
    """
    logger.warning("JWT token missing from request")
    return jsonify({
        'status': 'failed',
        'message': "JWT token is missing. Access denied."
    }), 401


@jwt_required()
def get_current_user():
    """
    Retrieve the current user based on the JWT token.

    :return: User's information.
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)  # Fetch complete user information
        return jsonify({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'roles': user.roles
        }), 200
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'Error fetching user', 'error': str(e)}), 500


def revoke_jwt_token(token_jti):
    """
    Revoke a JWT token by storing its JTI (JWT ID) in the revoked tokens table.

    :param token_jti: JTI of the token to revoke.
    """
    try:
        revoked_token = RevokedToken(jti=token_jti)
        revoked_token.add()
        logger.info(f"Token {token_jti} revoked successfully")
    except Exception as e:
        logger.error(f"Error revoking token: {str(e)}")


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Check if a JWT token has been revoked by querying the revoked tokens table.

    :param jwt_header: JWT header.
    :param jwt_payload: JWT payload.
    :return: Boolean indicating if the token is revoked.
    """
    jti = jwt_payload['jti']  # Unique identifier for the JWT token
    return RevokedToken.is_token_revoked(jti)
