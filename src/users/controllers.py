import logging
from flask import request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from src.extensions import db
from src.logs.models import Log

from src.middlewares.decorators import handle_exceptions
from src.tokens.services import revoke_jwt_token
from src.users.models import User
from src.users.services import *

# Logger configuration
logger = logging.getLogger(__name__)


@handle_exceptions
def signup():
    """
    Sign up a new user by creating a new account by calling the user service.
    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    role = data.get('role', 'user')  # Default role is 'user'
    tokens = signup_user(data, role=role)

    return jsonify({'status': "success", "message": "User Sign up Successful", "tokens": tokens}), 201


@handle_exceptions
def login():
    """
    Log in an existing user by verifying their credentials by calling the user service.
    :return: JSON response containing access and refresh tokens or indicating failure.
    """
    data = request.get_json()
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


@jwt_required()
@handle_exceptions
def logout():
    """
    Log out the current user by revoking their JWT token.
    :return: JSON response indicating successful logout.
    """
    jti = get_jwt()['jti']  # JWT ID
    current_user_identity = get_jwt_identity()

    # Revoke the JWT token
    revoke_jwt_token(jti)

    # Deactivate the user
    user_id = current_user_identity['user_id']
    user = User.query.get(user_id)

    if user:
        # Log the logout action
        log = Log(user_id=user_id, action="User logged out")
        log.save()

        user.is_active = False
        db.session.commit()

    logger.info(f"User logged out, token {jti} revoked, user_id {user_id} set to inactive")
    return jsonify({"message": "Successfully logged out"}), 200
