import os
from datetime import datetime
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from src import db
from src.services.jwt_service import create_jwt_token, revoke_jwt_token  # Refactoring to use services
from src.services.api_key_service import generate_api_key as generate_api_key_service  # Refactored to use API key service
from src.services.user_service import signup_user, login_user  # Refactored to use user service
import logging

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@jwt_required()
def generate_api_key():
    """
    Generate a new API key for the current user by calling the service function.

    :return: JSON response containing the new API key.
    """
    try:
        response = generate_api_key_service()
        return jsonify(response), 201
    except Exception as e:
        logger.error(f"Error generating API key: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'Error generating API key', 'error': str(e)}), 500

def signup():
    """
    Sign up a new user by creating a new account by calling the user service.

    :return: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        role = data.get('role', 'user')  # Default role is 'user'
        tokens = signup_user(data, role=role)
        return jsonify({'status': "success", "message": "User Sign up Successful", "tokens": tokens}), 201
    except ValueError as ve:
        return jsonify({'status': "failed", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        return jsonify({'status': "failed", "message": "An error occurred", 'error': str(e)}), 500

def login():
    """
    Log in an existing user by verifying their credentials by calling the user service.

    :return: JSON response containing access and refresh tokens or indicating failure.
    """
    try:
        data = request.get_json()
        tokens = login_user(data)
        return jsonify({'status': "success", "message": "User Login Successful", "tokens": tokens}), 200
    except ValueError as ve:
        return jsonify({'status': "failed", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({'status': "failed", "message": "An error occurred", 'error': str(e)}), 500

@jwt_required()
def logout():
    """
    Log out the current user by revoking their JWT token.

    :return: JSON response indicating successful logout.
    """
    try:
        jti = get_jwt()['jti']  # JWT ID
        revoke_jwt_token(jti)  # Appeler la fonction pour révoquer le token
        logger.info(f"User logged out, token {jti} revoked")
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred during logout', 'error': str(e)}), 500