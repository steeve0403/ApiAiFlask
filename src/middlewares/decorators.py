from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
import logging
from src.exceptions import UnauthorizedError, NotFoundError, ValidationError
from src.users.models import User

# Logger configuration
logger = logging.getLogger(__name__)

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
                # Retrieve user identity from the JWT
                user_identity = get_jwt_identity()
                user = User.query.filter_by(id=user_identity['user_id']).first()

                if user is None:
                    logger.warning("User not found while trying to access a role-protected resource.")
                    raise NotFoundError("User not found")

                if user.role != required_role:
                    logger.warning(
                        f"User with role {user.role} attempted to access a {required_role} resource."
                    )
                    raise UnauthorizedError("You do not have the required role.")

                logger.info(f"User with role {user.role} accessed a {required_role} resource.")
                return f(*args, **kwargs)
            except UnauthorizedError as ue:
                return jsonify({"msg": str(ue)}), 403
            except NotFoundError as ne:
                return jsonify({"msg": str(ne)}), 404
            except Exception as e:
                logger.error(f"Error in role_required decorator: {str(e)}")
                return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500

        return wrapper

    return decorator

def handle_exceptions(f):
    """
    Custom decorator to handle exceptions in the wrapped function.
    :param f: The function to wrap.
    :return: Decorated function that handles exceptions.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except UnauthorizedError as ue:
            return jsonify({"msg": str(ue)}), 403
        except NotFoundError as ne:
            return jsonify({"msg": str(ne)}), 404
        except ValidationError as ve:
            return jsonify({"msg": str(ve)}), 400
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}")
            return jsonify({'status': 'failed', 'message': 'An unexpected error occurred', 'error': str(e)}), 500
    return wrapper

