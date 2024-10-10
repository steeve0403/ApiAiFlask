from flask import Blueprint, jsonify
from src.controllers.user_controller import signup, login, logout, generate_api_key
from src.middlewares.decorators import role_required
from flask_jwt_extended import jwt_required
import logging

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

auth_bp = Blueprint('auth', __name__)

# Route for registration
auth_bp.route('/signup', methods=['POST'])(signup)

# Route for login
auth_bp.route('/signin', methods=['POST'])(login)

# Route for logout
auth_bp.route('/logout', methods=['POST'])(logout)

# Route for generating an API key
auth_bp.route('/generate-api-key', methods=['POST'])(generate_api_key)

# Route reserved for administrators
@auth_bp.route('/admin/dashboard', methods=['GET'])

@jwt_required()
@role_required('admin')  # Verify admin role before allowing access
def admin_dashboard():
    """
    Admin dashboard endpoint (placeholder).

    :return: JSON response indicating success.
    """
    try:
        logger.info("Admin dashboard accessed")
        return jsonify({"message": "Welcome to the admin dashboard"}), 200
    except Exception as e:
        logger.error(f"Error accessing admin dashboard: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An error occurred', 'error': str(e)}), 500


"""
curl -X POST http://127.0.0.1:5000/api/auth/signin -H "Content-Type: application/json" -d '{"firstname": "Steeve", "lastname": "Zych", "email": "zychsteeve4@gmail.com", "password": "azerty123"}'
"""