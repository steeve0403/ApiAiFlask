from flask_jwt_extended import get_jwt_identity
from src.models.api_key_model import ApiKeyModel
from src.exceptions import NotFoundError, ValidationError
import logging

# Logger configuration
logger = logging.getLogger(__name__)


def generate_api_key_service():
    """
    Generate a new API key for the current user.

    :return: Dictionary containing the new API key.
    """
    try:
        current_user = get_jwt_identity()
        current_user_id = current_user.get('user_id')
        if not current_user_id:
            raise ValidationError("User identity not found in JWT token")

        new_api_key = ApiKeyModel(user_id=current_user_id)
        new_api_key.save()
        logger.info(f"API key generated for user_id {current_user_id}: {new_api_key.key}")
        return {'api_key': new_api_key.key}
    except Exception as e:
        logger.error(f"Error generating API key: {str(e)}")
        raise


def validate_api_key_service(api_key, user_id):
    """
    Validate if the API key belongs to the given user.

    :param api_key: The API key to validate.
    :param user_id: The ID of the user to check ownership.
    :return: True if the API key belongs to the user, False otherwise.
    """
    try:
        api_key_record = ApiKeyModel.query.filter_by(key=api_key, user_id=user_id).first()
        if not api_key_record:
            raise NotFoundError("API key not found for the given user")
        return True
    except Exception as e:
        logger.error(f"Error validating API key: {str(e)}")
        raise


def get_user_api_keys_service():
    """
    Get all API keys associated with the current user.

    :return: Dictionary containing the list of API keys.
    """
    try:
        current_user = get_jwt_identity()
        current_user_id = current_user.get('user_id')
        if not current_user_id:
            raise ValidationError("User identity not found in JWT token")

        api_keys = ApiKeyModel.query.filter_by(user_id=current_user_id).all()
        keys = [api_key.key for api_key in api_keys]
        logger.info(f"Retrieved {len(keys)} API keys for user_id {current_user_id}")
        return {'api_keys': keys}
    except Exception as e:
        logger.error(f"Error retrieving API keys: {str(e)}")
        raise
