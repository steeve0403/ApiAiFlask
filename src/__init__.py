import logging
from flask import Flask
import os
from dotenv import load_dotenv
from src.config.config import get_config
from src.extensions import db, migrate, bcrypt, jwt
from src.error_handler import *
from src.routes import register_blueprints
from flask_restx import Api

# Load environment variables
load_dotenv()

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Declare the app
def create_app():
    app = Flask(__name__)

    api = Api(app, version='1.0', title='Api AI Flask', description='A simple Flask API for managing AI models and interact with them.')

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
    register_blueprints(app)

    return app


app = create_app()
