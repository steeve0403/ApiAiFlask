from flask import Flask, render_template
import os
from dotenv import load_dotenv
from flask_cors import CORS

from src.config.config import get_config
from src.extensions import db, migrate, bcrypt, jwt
from src.error_handler import *
from flask_restx import Api

# Import Blueprint for redoc
from src.views.redoc import redoc_bp

# Load environment variables
load_dotenv()

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Declare the app
def create_app():
    app = Flask(__name__)

    # Enable CORS only for documentation
    # CORS(app, resources={r"/swagger/*": {"origins": "*"}, r"/redoc": {"origins": "*"}})

    api = Api(app,
              version='1.0',
              title='Api AI Flask Documentation',
              description='A simple Flask API for managing AI models and interact with them.',
              contact='example@gmail.com',
              license='MIT',
    )

    # Load the appropriate configuration based on the environment
    config = get_config()
    app.config.from_object(config)

    # Load the secret key defined in the .env file
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Import models to let the migrate tool know about them
    from src.users.models import User
    from src.tokens.models import RevokedToken
    from src.logs.models import Log
    from src.api_keys.models import ApiKeyModel

    # Register Blueprints
    from src.routes import register_blueprints
    register_blueprints(app)
    app.register_blueprint(redoc_bp)

    # Import namespaces and add them to the API
    # from src.users.namespaces import users_ns
    # from src.admin.namespaces import admin_ns
    # from src.api_keys.namespaces import api_keys_ns
    #
    # api.add_namespace(users_ns, path='/api/users')
    # api.add_namespace(admin_ns, path='/api/admin')
    # api.add_namespace(api_keys_ns, path='/api/keys')



    return app


app = create_app()
