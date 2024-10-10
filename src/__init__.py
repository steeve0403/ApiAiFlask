from flask import Flask
import os
from dotenv import load_dotenv
from src.config.config import get_config
import logging
from src.extensions import db, migrate, bcrypt, jwt

# Load environment variables
load_dotenv()

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Declare the app
app = Flask(__name__)

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

# Import models to let the migrate tool know about them
from src.models.user_model import User
from src.models.token_model import RevokedToken

# Import and register Blueprints
from src.routes import auth_bp, api_key_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(api_key_bp, url_prefix='/api/keys')
