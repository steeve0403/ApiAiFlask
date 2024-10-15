import logging
from flask import jsonify
from flask_jwt_extended import jwt_required
from src.services.admin_service import (
    list_all_users_service, activate_user_service, deactivate_user_service, view_user_logs_service
)
from src.middlewares.decorators import role_required, handle_exceptions

# Logger configuration
logger = logging.getLogger(__name__)

@jwt_required()
@role_required('admin')
@handle_exceptions
def admin_dashboard():
    logger.info('Admin dashboard accessed')
    return jsonify({'status': 'success', 'message': 'Welcome to the admin dashboard'}), 200

@jwt_required()
@role_required('admin')
@handle_exceptions
def list_users():
    users = list_all_users_service()
    return jsonify({'status': 'success', 'users': users}), 200

@jwt_required()
@role_required('admin')
@handle_exceptions
def deactivate_user(user_id):
    response = deactivate_user_service(user_id)
    return jsonify(response), 200

@jwt_required()
@role_required('admin')
@handle_exceptions
def activate_user(user_id):
    response = activate_user_service(user_id)
    return jsonify(response), 200

@jwt_required()
@role_required('admin')
@handle_exceptions
def view_user_logs():
    logs = view_user_logs_service()
    return jsonify({'status': 'success', 'logs': logs}), 200
