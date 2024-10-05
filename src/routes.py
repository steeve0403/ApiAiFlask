from flask import Blueprint
from src.controllers.user_controller import handle_signup, handle_login, admin_dashboard
from src.middlewares.decorators import role_required
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

# Route pour l'inscription
auth_bp.route('/signup', methods=['POST'])(handle_signup)

# Route pour la connexion
auth_bp.route('/signin', methods=['POST'])(handle_login)

# Route réservée aux administrateurs
@auth_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')  # Vérification du rôle admin avant d'autoriser l'accès
def admin_dashboard():
    return admin_dashboard()
