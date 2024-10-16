from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from src.admin.services import *
import logging

# Logger configuration
logger = logging.getLogger(__name__)

# Create Namespace for admin
admin_ns = Namespace('admin', description='Admin related operations', tags=['admin'])

# Define models for input/output with Flask-RESTX
user_action_response_model = admin_ns.model('UserActionResponse', {
    'status': fields.String(description='Status of the response'),
    'message': fields.String(description='Message of the response')
})

user_list_model = admin_ns.model('UserList', {
    'status': fields.String(description='Status of the response'),
    'users': fields.List(fields.Raw, description='List of users')
})

log_list_model = admin_ns.model('LogList', {
    'status': fields.String(description='Status of the response'),
    'logs': fields.List(fields.Raw, description='List of user activity logs')
})


# Admin Dashboard Resource
@admin_ns.route('/dashboard')
class AdminDashboard(Resource):
    @jwt_required()
    @admin_ns.response(200, 'Welcome to the admin dashboard')
    def get(self):
        """
        Access the admin dashboard
        """
        logger.info('Admin dashboard accessed')
        return {'status': 'success', 'message': 'Welcome to the admin dashboard'}, 200


# List Users Resource
@admin_ns.route('/users')
class ListUsers(Resource):
    @jwt_required()
    @admin_ns.response(200, 'Successfully retrieved user list', user_list_model)
    @admin_ns.response(500, 'Failed to retrieve user list')
    def get(self):
        """
        List all users in the system
        """
        users = list_all_users_service()
        return {'status': 'success', 'users': users}, 200


# Deactivate User Resource
@admin_ns.route('/users/<int:user_id>/deactivate')
class DeactivateUser(Resource):
    @jwt_required()
    @admin_ns.response(200, 'User successfully deactivated', user_action_response_model)
    @admin_ns.response(404, 'User not found')
    def put(self, user_id):
        """
        Deactivate a user by user ID
        """
        response = deactivate_user_service(user_id)
        return response, 200


# Activate User Resource
@admin_ns.route('/users/<int:user_id>/activate')
class ActivateUser(Resource):
    @jwt_required()
    @admin_ns.response(200, 'User successfully activated', user_action_response_model)
    @admin_ns.response(404, 'User not found')
    def put(self, user_id):
        """
        Activate a user by user ID
        """
        response = activate_user_service(user_id)
        return response, 200


# View User Logs Resource
@admin_ns.route('/logs')
class ViewUserLogs(Resource):
    @jwt_required()
    @admin_ns.response(200, 'Successfully retrieved user logs', log_list_model)
    @admin_ns.response(500, 'Failed to retrieve logs')
    def get(self):
        """
        View logs of user activities
        """
        logs = view_user_logs_service()
        return {'status': 'success', 'logs': logs}, 200
