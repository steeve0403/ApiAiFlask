from flask_jwt_extended import get_jwt_identity
from src.models.api_key_model import ApiKeyModel
import logging

# Logger configuration
logger = logging.getLogger(__name__)

def generate_api_key_service():
    """
    Generate a new API key for the current user.

    :return: Dictionary containing the new API key.
    """
    try:
        current_user_id = get_jwt_identity()
        new_api_key = ApiKeyModel(user_id=current_user_id)
        new_api_key.save()
        logger.info(f"API key generated for user_id {current_user_id}: {new_api_key.key}")
        return {'api_key': new_api_key.key}
    except Exception as e:
        logger.error(f"Error generating API key: {str(e)}")
        raise

def get_user_api_keys_service():
    """
    Get all API keys associated with the current user.

    :return: Dictionary containing the list of API keys.
    """
    try:
        current_user_id = get_jwt_identity()
        api_keys = ApiKeyModel.query.filter_by(user_id=current_user_id).all()
        keys = [api_key.key for api_key in api_keys]
        logger.info(f"Retrieved {len(keys)} API keys for user_id {current_user_id}")
        return {'api_keys': keys}
    except Exception as e:
        logger.error(f"Error retrieving API keys: {str(e)}")
        raise
