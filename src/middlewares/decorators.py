from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
import logging
from src.models.user_model import User  # Import User model to check role from the database

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def role_required(required_role):
    """
    Custom decorator to check if the user has the required role.
    :param required_role: The role required to access the resource.
    :return: Decorator function.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user_identity = get_jwt_identity()  # Retrieve user identity from the JWT
                user = User.query.filter_by(id=user_identity['user_id']).first()
                if user is None or user.role != required_role:
                    logger.warning(
                        f"User with role {user.role if user else 'unknown'} attempted to access a {required_role} resource.")
                    return jsonify({"msg": "You do not have the required role"}), 403
                logger.info(f"User with role {user.role} accessed a {required_role} resource.")
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in role_required decorator: {str(e)}")
                return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500

        return wrapper

    return decorator
