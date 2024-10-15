import logging
from flask import Blueprint
from src.users.controllers import *
from src.admin.controllers import *
from src.api_keys.controllers import *

# Logger configuration
logger = logging.getLogger(__name__)


# Function to add multiple routes to a Blueprint
def add_routes(blueprint, routes):
    for route, methods, view_func in routes:
        blueprint.add_url_rule(route, methods=methods, view_func=view_func)
        logger.info(f"Added route: {route} added to {blueprint.name} with methods: {methods}")


# Function to register blueprints
def register_blueprints(app):
    # Auth Blueprint
    auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
    auth_routes = [
        ('/signup', ['POST'], signup),
        ('/signin', ['POST'], login),
        ('/logout', ['POST'], logout)
    ]
    add_routes(auth_bp, auth_routes)

    # Admin Blueprint
    admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
    admin_routes = [
        ('/dashboard', ['GET'], admin_dashboard),
        ('/users', ['GET'], list_users),
        ('/users/<int:user_id>/deactivate', ['PUT'], deactivate_user),
        ('/users/<int:user_id>/activate', ['PUT'], activate_user),
        ('/logs', ['GET'], view_user_logs)
    ]
    add_routes(admin_bp, admin_routes)

    # API Keys Blueprint
    api_key_bp = Blueprint('api_keys', __name__, url_prefix='/api/keys')
    api_key_routes = [
        ('/generate', ['POST'], generate_api_key),
        ('/all', ['GET'], get_user_api_keys)
    ]
    add_routes(api_key_bp, api_key_routes)

    # Register blueprints with the Flask app
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_key_bp)
