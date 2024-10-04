from flask import Flask
import os
from src.config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Declare the app
app = Flask(__name__)

# Calling the dev config
config = Config().dev_config()

# Making our app to use dev env
app.env = config.ENV