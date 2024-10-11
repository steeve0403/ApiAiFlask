from flask import Blueprint, jsonify

from src.controllers.admin_controller import admin_dashboard, list_users, deactivate_user, activate_user, view_user_logs
from src.controllers.api_key_controller import get_user_api_keys, generate_api_key
from src.controllers.user_controller import signup, login, logout
from src.middlewares.decorators import role_required
from flask_jwt_extended import jwt_required
import logging

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Auth Blueprint
auth_bp = Blueprint('auth', __name__)

# Route for registration
auth_bp.route('/signup', methods=['POST'])(signup)

# Route for login
auth_bp.route('/signin', methods=['POST'])(login)

# Route for logout
auth_bp.route('/logout', methods=['POST'])(logout)

# Routes for admin users
auth_bp.route('/admin/dashboard', methods=['GET'])(admin_dashboard)
auth_bp.route('/admin/users', methods=['GET'])(list_users)
auth_bp.route('/admin/users/<int:user_id>/deactivate', methods=['PUT'])(deactivate_user)
auth_bp.route('/admin/users/<int:user_id>/activate', methods=['PUT'])(activate_user)
auth_bp.route('/admin/logs', methods=['GET'])(view_user_logs)

# API Keys Blueprint
api_key_bp = Blueprint('api_keys', __name__)

# Route for generating an API key
api_key_bp.route('/generate', methods=['POST'])(generate_api_key)

# Route for getting user API keys
api_key_bp.route('/all', methods=['GET'])(get_user_api_keys)

