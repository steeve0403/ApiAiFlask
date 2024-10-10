from flask import jsonify
from src.services.admin_service import get_dashboard_stats, get_all_users, change_user_role
from flask_jwt_extended import jwt_required
from src.middlewares.decorators import role_required
import logging

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@jwt_required()
@role_required('admin')
def admin_dashboard():
    """
    Admin dashboard endpoint to provide an overview.

    :return: JSON response indicating success.
    """
    try:
        statistics = get_dashboard_stats()
        logger.info("Admin dashboard accessed")
        return jsonify({"message": "Welcome to the admin dashboard", "statistics": statistics}), 200
    except Exception as e:
        logger.error(f"Error accessing admin dashboard: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500


@jwt_required()
@role_required('admin')
def list_users():
    """
    Get a list of all users.

    :return: JSON response with user data.
    """
    try:
        users = get_all_users()
        users_list = [
            {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in users
        ]
        return jsonify({"status": "success", "users": users_list}), 200
    except Exception as e:
        logger.error(f"Error fetching users list: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500


@jwt_required()
@role_required('admin')
def deactivate_user(user_id):
    """
    Deactivate a user by setting their role to 'inactive'.

    :param user_id: ID of the user to deactivate.
    :return: JSON response indicating the result.
    """
    try:
        user = change_user_role(user_id, 'inactive')
        if not user:
            return jsonify({"status": "failed", "message": "User not found"}), 404

        logger.info(f"User {user.email} deactivated successfully")
        return jsonify({"status": "success", "message": f"User {user.email} deactivated"}), 200
    except Exception as e:
        logger.error(f"Error deactivating user: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500


@jwt_required()
@role_required('admin')
def activate_user(user_id):
    """
    Reactivate a user by setting their role back to 'user'.

    :param user_id: ID of the user to activate.
    :return: JSON response indicating the result.
    """
    try:
        user = change_user_role(user_id, 'user')
        if not user:
            return jsonify({"status": "failed", "message": "User not found"}), 404

        logger.info(f"User {user.email} reactivated successfully")
        return jsonify({"status": "success", "message": f"User {user.email} reactivated"}), 200
    except Exception as e:
        logger.error(f"Error activating user: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500
