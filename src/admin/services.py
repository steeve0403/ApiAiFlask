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
        user_list = [user.to_dict() for user in users]
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

    def deactivate_user_service(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                raise NotFoundError("User not found")

            if not user.is_active:
                raise ValidationError(f"User {user_id} is already deactivated.")

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


def view_user_logs_service(page=1, per_page=20):
    """
    Retrieve user activity logs with pagination.

    :param page: The page number.
    :param per_page: Number of logs per page.
    :return: List of user activity logs.
    """
    try:
        logs = Log.query.paginate(page=page, per_page=per_page, error_out=False)
        log_list = [
            {
                'user_id': log.user_id,
                'action': log.action,
                'timestamp': log.timestamp.isoformat()
            }
            for log in logs.items
        ]
        logger.info(f"Retrieved {len(log_list)} logs")
        return log_list
    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        raise ValidationError("Failed to retrieve logs.")
