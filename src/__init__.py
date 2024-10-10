from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from src.config.config import get_config
import logging

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
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models to let the migrate tool know about them
from src.models.user_model import User
from src.models.token_model import RevokedToken

# Import and register Blueprints
from src.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix=config.API_BASE_PATH)
