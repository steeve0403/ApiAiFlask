from flask import jsonify
from flask_jwt_extended import jwt_required
from src.services.api_key_service import generate_api_key_service, get_user_api_keys_service
from src.exceptions import AppErrorBaseClass, ValidationError
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
    except AppErrorBaseClass as e:
        logger.error(f"Error generating API key: {str(e)}")
        return jsonify({'status': 'failed', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error generating API key: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An unexpected error occurred while generating the API key',
                        'error': str(e)}), 500


@jwt_required()
def get_user_api_keys():
    """
    Get all API keys associated with the current user.

    :return: JSON response containing all API keys.
    """
    try:
        response = get_user_api_keys_service()
        return jsonify(response), 200
    except AppErrorBaseClass as e:
        logger.error(f"Error retrieving API keys: {str(e)}")
        return jsonify({'status': 'failed', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error retrieving API keys: {str(e)}")
        return jsonify({'status': 'failed', 'message': 'An unexpected error occurred while retrieving the API keys',
                        'error': str(e)}), 500
