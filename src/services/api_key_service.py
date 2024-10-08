from src.models.api_key_model import ApiKeyModel
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
import logging

# Logger configuration
logger = logging.getLogger(__name__)


def generate_api_key():
    """
    Generate a new API key for the current user.

    :return: Dictionary containing the new API key.
    """
    try:
        current_user_id = get_jwt_identity()
        new_api_key = ApiKeyModel(user_id=current_user_id)
        new_api_key.save()
        logger.info(f"API key generated for user {current_user_id}")
        return {'api-key': new_api_key.key}
    except Exception as e:
        logger.error(f"Error generating API key: {str(e)}")
        raise e
