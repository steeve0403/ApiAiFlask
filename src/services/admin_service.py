import logging
from sqlalchemy.orm import load_only
from src.models.user_model import User
from src.models.log_model import Log
from src import db
from src.exceptions import UserNotFoundError, DatabaseError

# Logger configuration
logger = logging.getLogger(__name__)


def list_all_users_service():
    """
    Retrieve a list of all users.

    :return: List of dictionaries containing user details.
    """
    try:
        # Optimize the query to load only the necessary columns
        users = User.query.options(load_only['id', 'firstname', 'lastname', 'email', 'role', 'is_active']).all()
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
        logger.info(f"Retrieved {len(user_list)} users")
        return user_list
    except Exception as e:
        logger.error(f"Error listing all users: {str(e)}")
        raise DatabaseError("Failed to list all users")


def deactivate_user_service(user_id):
    """
    Deactivate a user account.

    :param user_id: ID of the user to deactivate.
    :return: Dictionary indicating the status of the operation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")

        user.is_active = False
        db.session.commit()
        logger.info(f"User {user_id} deactivated successfully")
        return {'status': 'success', 'message': f"User {user_id} deactivated successfully"}
    except UserNotFoundError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error deactivating user {user_id}: {str(e)}")
        db.session.rollback()
        raise DatabaseError(f"Failed to deactivate user {user_id}")


def activate_user_service(user_id):
    """
    Activate a user account.

    :param user_id: ID of the user to activate.
    :return: Dictionary indicating the status of the operation.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")

        user.is_active = True
        db.session.commit()
        logger.info(f"User {user_id} activated successfully")
        return {'status': 'success', 'message': f"User {user_id} activated successfully"}
    except UserNotFoundError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Error activating user {user_id}: {str(e)}")
        db.session.rollback()
        raise DatabaseError(f"Failed to activate user {user_id}")


def view_user_logs_service():
    """
    Retrieve user activity logs.

    :return: List of user activity logs.
    """
    try:
        # Load only the necessary information on the logs
        logs = Log.query.options(load_only['user_id', 'action', 'timestamp']).all()
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
        raise DatabaseError("Failed to retrieve user activity logs")
