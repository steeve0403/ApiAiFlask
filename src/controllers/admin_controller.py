import logging

from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.services.admin_service import list_all_users_service, activate_user_service, deactivate_user_service, view_user_logs_service
from src.middlewares.decorators import role_required

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@jwt_required()
@role_required('admin')
def admin_dashboard():
    try:
        logger.info("Admin dashboard accessed")
        return jsonify({"message": "Welcome to the admin dashboard"}), 200
    except Exception as e:
        logger.error(f"Error accessing admin dashboard: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500

@jwt_required()
@role_required('admin')
def list_users():
    try:
        users = list_all_users_service()
        return jsonify({'status': 'success', 'users': users}), 200
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500

@jwt_required()
@role_required('admin')
def deactivate_user(user_id):
    try:
        response = deactivate_user_service(user_id)
        return jsonify(response), 200
    except ValueError as ve:
        logger.error(f"Validation error during deactivating user: {str(ve)}")
        return jsonify({'status': 'failed', 'message': str(ve)}), 400
    except Exception as e:
        logger.error(f"Error deactivating user: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500

@jwt_required()
@role_required('admin')
def activate_user(user_id):
    try:
        response = activate_user_service(user_id)
        return jsonify(response), 200
    except ValueError as ve:
        logger.error(f"Validation error during activating user: {str(ve)}")
        return jsonify({'status': 'failed', 'message': str(ve)}), 400
    except Exception as e:
        logger.error(f"Error activating user: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500

@jwt_required()
@role_required('admin')
def view_user_logs():
    """
    View logs of user activities.

    :return: JSON response containing logs.
    """
    try:
        logs = view_user_logs_service()
        return jsonify({'status': 'success', 'logs': logs}), 200
    except Exception as e:
        logger.error(f"Error viewing user logs: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500
