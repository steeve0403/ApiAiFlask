from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Declare the app
app = Flask(__name__)

# Calling the dev config
config = Config().dev_config

# Making our app to use dev env
app.env = config.ENV

# Path for loccal sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')

# To specify the track modifications of objects and emit signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

# Sqlalchemy instance
db = SQLAlchemy(app)

# Flask migrate instance to handle db migrations
migrate = Migrate(app, db)

# Import models to let the migrate tool know
from src.models.user_model import User


# Import api Blueprint to register it with the app
from src.routes import api
app.register_blueprint(api, url_prefix="/api")