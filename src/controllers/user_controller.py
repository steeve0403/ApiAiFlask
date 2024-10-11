import logging

from flask import request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity

from src import db
from src.models.user_model import User
from src.models.log_model import Log
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

        required_fields = ["firstname", "lastname", "email", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing required field: {field}")

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

        # Log the login action
        user_email = data.get('email')
        user = User.query.filter_by(email=user_email).first()
        if user:
            log = Log(user_id=user.id, action="User logged in")
            log.save()

            # Activate the user if they are not active
            user.is_active = True
            user.save()

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
        current_user_identity = get_jwt_identity()

        # Revoke the JWT token
        revoke_jwt_token(jti)

        # Deactivate the user
        user_id = current_user_identity['user_id']
        user = User.query.get(user_id)

        if user:
            # Log the logout action
            log = Log(user_id=current_user_identity, action="User logged out")
            log.save()

            user.is_active = False
            db.session.commit()

            logger.info(f"User logged out, token {jti} revoked, user_id {user_id} set to inactive")
            return jsonify({"message": "Successfully logged out"}), 200
        else:
            raise ValueError("User not found")

    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return jsonify(
            {'status': 'failed', 'message': 'An unexpected error occurred during logout', 'error': str(e)}), 500
