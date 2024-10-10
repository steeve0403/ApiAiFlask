import logging

from flask import request, jsonify
from flask_jwt_extended import get_jwt, jwt_required

from src.services.jwt_service import revoke_jwt_token  # Refactoring to use services
from src.services.user_service import signup_user, login_user  # Refactored to use user service

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def signup():
    """
    Sign up a new user by creating a new account by calling the user service.
    :return: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Invalid input data. JSON is required.")

        role = data.get('role', 'user')  # Default role is 'user'
        tokens = signup_user(data, role=role)
        return jsonify({'status': "success", "message": "User Sign up Successful", "tokens": tokens}), 201
    except ValueError as ve:
        logger.error(f"Validation error during signup: {str(ve)}")
        return jsonify({'status': "failed", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        return jsonify({'status': "failed", "message": "An unexpected error occurred", 'error': str(e)}), 500


def login():
    """
    Log in an existing user by verifying their credentials by calling the user service.
    :return: JSON response containing access and refresh tokens or indicating failure.
    """
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Invalid input data. JSON is required.")

        tokens = login_user(data)
        return jsonify({'status': "success", "message": "User Login Successful", "tokens": tokens}), 200
    except ValueError as ve:
        logger.error(f"Validation error during login: {str(ve)}")
        return jsonify({'status': "failed", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return jsonify({'status': "failed", "message": "An unexpected error occurred", 'error': str(e)}), 500


@jwt_required()
def logout():
    """
    Log out the current user by revoking their JWT token.
    :return: JSON response indicating successful logout.
    """
    try:
        jti = get_jwt()['jti']  # JWT ID
        revoke_jwt_token(jti)
        logger.info(f"User logged out, token {jti} revoked")
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return jsonify(
            {'status': 'failed', 'message': 'An unexpected error occurred during logout', 'error': str(e)}), 500
