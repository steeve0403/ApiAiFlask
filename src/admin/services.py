import logging

from src import db
from src.exceptions import NotFoundError, ValidationError
from src.logs.models import Log
from src.users.models import User

# Logger configuration
logger = logging.getLogger(__name__)


def list_all_users_service():
    """
    Retrieve all users in the system.

    :return: List of users with their details.
    """
    try:
        users = User.query.all()
        user_list = [
            {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'role': user.role,
                'active': user.is_active
            }
            for user in users
        ]
        return user_list
    except Exception as e:
        logger.error(f"Error listing all users: {str(e)}")
        raise ValidationError("Failed to retrieve user list.")


def deactivate_user_service(user_id):
    """
    Deactivate a user by setting their active status to False.

    :param user_id: ID of the user to deactivate.
    :return: Status message indicating the deactivation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_active = False
        db.session.commit()
        logger.info(f"User {user_id} deactivated")
        return {'status': 'success', 'message': f"User {user_id} deactivated successfully"}
    except NotFoundError as e:
        logger.warning(f"Deactivation failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error deactivating user {user_id}: {str(e)}")
        db.session.rollback()
        raise ValidationError("Failed to deactivate user.")


def activate_user_service(user_id):
    """
    Activate a user by setting their active status to True.

    :param user_id: ID of the user to activate.
    :return: Status message indicating the activation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_active = True
        db.session.commit()
        logger.info(f"User {user_id} activated")
        return {'status': 'success', 'message': f"User {user_id} activated successfully"}
    except NotFoundError as e:
        logger.warning(f"Activation failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error activating user {user_id}: {str(e)}")
        db.session.rollback()
        raise ValidationError("Failed to activate user.")


def view_user_logs_service():
    """
    Retrieve user activity logs.

    :return: List of user activity logs.
    """
    try:
        logs = Log.query.all()  # Assuming we have a Log model for storing activity logs
        log_list = [
            {
                'user_id': log.user_id,
                'action': log.action,
                'timestamp': log.timestamp
            }
            for log in logs
        ]
        logger.info(f"Retrieved {len(log_list)} logs")
        return log_list
    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        raise ValidationError("Failed to retrieve logs.")
