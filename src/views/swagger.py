from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI setup
SWAGGER_URL = '/swagger'  # The URL for Swagger UI
API_URL = '/swagger.json'  # The JSON file with the OpenAPI/Swagger specs

# Create a Swagger Blueprint
swagger_bp = Blueprint('swagger_ui', __name__)

# Configure the Swagger UI blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask AI API Documentation"
    }
)

# Register the Swagger UI blueprint
swagger_bp.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
