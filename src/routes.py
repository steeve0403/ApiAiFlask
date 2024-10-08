from flask import Blueprint
from src.controllers.user_controller import signup, login, logout, generate_api_key
from src.middlewares.decorators import role_required
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

# Route for registration
auth_bp.route('/signup', methods=['POST'])(signup)

# Route for connexion
auth_bp.route('/signin', methods=['POST'])(login)

# Route for logout
auth_bp.route('/logout', methods=['POST'])(logout)

# Route for generating an API key
auth_bp.route('generate', methods=['POST'])(generate_api_key)


# Route réservée aux administrateurs
@auth_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')  # Vérification du rôle admin avant d'autoriser l'accès
def admin_dashboard():
    return admin_dashboard()
