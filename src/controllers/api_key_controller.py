from flask import jsonify
from flask_jwt_extended import jwt_required
from src.services.api_key_service import generate_api_key_service, get_user_api_keys_service
import logging

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@jwt_required()
def generate_api_key():
    """
    Generate a new API key for the current user by calling the service function.

    :return: JSON response containing the new API key.
    """
    try:
        response = generate_api_key_service()
        return jsonify(response), 201
    except Exception as e:
        logger.error(f"Error generating API key: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'Error generating API key', 'error': str(e)}), 500


@jwt_required()
def get_user_api_keys():
    """
    Get all API keys associated with the current user.

    :return: JSON response containing all API keys.
    """
    try:
        response = get_user_api_keys_service()
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error retrieving API keys: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'Error retrieving API keys', 'error': str(e)}), 500
