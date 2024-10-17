from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI setup
SWAGGER_URL = '/swagger'  # The URL for Swagger UI
API_URL = '/swagger.json'  # The JSON file with the OpenAPI/Swagger specs

swagger_bp = Blueprint('swagger', __name__)

# Configure the Swagger UI blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask AI API Documentation"
    }
)
