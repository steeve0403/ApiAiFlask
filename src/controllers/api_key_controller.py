import logging
from flask import jsonify
from flask_jwt_extended import jwt_required
from src.services.api_key_service import generate_api_key_service, get_user_api_keys_service, delete_api_key_service, \
    verify_api_key_service
from src.middlewares.decorators import handle_exceptions

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@jwt_required()
@handle_exceptions
def generate_api_key():
    """
    Generate a new API key for the current user by calling the service function.
    :return: JSON response containing the new API key.
    """
    response = generate_api_key_service()
    return jsonify(response), 201

@jwt_required()
@handle_exceptions
def get_user_api_keys():
    """
    Get all API keys associated with the current user.
    :return: JSON response containing all API keys.
    """
    response = get_user_api_keys_service()
    return jsonify(response), 200

@jwt_required()
@handle_exceptions
def delete_api_key(api_key):
    """
    Delete an API key for the current user.
    :param api_key: The API key to delete.
    :return: JSON response indicating success or failure.
    """
    response = delete_api_key_service(api_key)
    return jsonify(response), 200

@jwt_required()
@handle_exceptions
def verify_api_key(api_key):
    """
    Verify if the provided API key is valid and active.
    :param api_key: The API key to verify.
    :return: JSON response indicating whether the key is valid or not.
    """
    response = verify_api_key_service(api_key)
    return jsonify(response), 200
