from flask import Flask
import os
from dotenv import load_dotenv
from flask_restx import Api

from src.config.config import get_config
from src.extensions import init_extensions
from src.error_handler import register_error_handlers
from src.views.redoc import redoc_bp
from flask_cors import CORS

# Load environment variables
load_dotenv()


# Declare the app
def create_app():
    app = Flask(__name__)

    # Enable CORS for documentation access
    CORS(app, resources={r"/swagger/*": {"origins": "*"}, r"/redoc/*": {"origins": "*"}})

    # Initialize the API with Swagger support via Flask-Restx
    api = Api(app,
              version='1.0',
              title='Flask AI API',
              description='API for managing AI models and user authentication.',
              doc='/swagger'  # Swagger UI available at /swagger
              )

    # Load the appropriate configuration based on the environment
    app.config.from_object(get_config())

    # Ensure the secret keys are properly set
    app.secret_key = app.config.get('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY')

    # Initialize extensions
    init_extensions(app)

    # Register error handlers
    register_error_handlers(app)

    # Import and register namespaces from src
    from src.users.namespaces import users_ns
    from src.admin.namespaces import admin_ns
    from src.api_keys.namespaces import api_keys_ns
    from src.tokens.namespaces import token_ns

    # Register namespaces with paths
    api.add_namespace(users_ns, path='/api/users')
    api.add_namespace(admin_ns, path='/api/admin')
    api.add_namespace(api_keys_ns, path='/api/keys')
    api.add_namespace(token_ns, path='/api/tokens')

    # Register Redoc blueprint
    app.register_blueprint(redoc_bp)


    # Register custom routes from routes.py
    from src.routes import register_blueprints
    register_blueprints(app)

    return app


app = create_app()
