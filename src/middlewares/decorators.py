from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


def role_required(required_role):
    """
    Custom decorator to check if the user has the required role.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()  # Retrieve user identity from the JWT
            if user['role'] != required_role:
                return jsonify({"msg": "You do not have the required role"}), 403
            return f(*args, **kwargs)

        return wrapper

    return decorator
