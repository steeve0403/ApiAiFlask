import logging
from src.models.user_model import User
from src.models.log_model import Log
from src import db

# Logger configuration
logger = logging.getLogger(__name__)


def list_all_users_service():
    try:
        users = User.query.all()
        user_list = [{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'email': user.email,
                      'role': user.role, 'active': user.is_active} for user in users]
        return user_list
    except Exception as e:
        logger.error(f"Error listing all users: {str(e)}")
        raise


def deactivate_user_service(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        user.is_active = False
        db.session.commit()
        logger.info(f"User {user_id} deactivated")
        return {'status': 'success', 'message': f"User {user_id} deactivated successfully"}
    except Exception as e:
        logger.error(f"Error deactivating user {user_id}: {str(e)}")
        db.session.rollback()
        raise


def activate_user_service(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        user.is_active = True
        db.session.commit()
        logger.info(f"User {user_id} activated")
        return {'status': 'success', 'message': f"User {user_id} activated successfully"}
    except Exception as e:
        logger.error(f"Error activating user {user_id}: {str(e)}")
        db.session.rollback()
        raise


def view_user_logs_service():
    """
    Retrieve user activity logs.

    :return: List of user activity logs.
    """
    try:
        logs = Log.query.all()  # Assuming we have a Log model for storing activity logs
        log_list = [{'user_id': log.user_id, 'action': log.action, 'timestamp': log.timestamp} for log in logs]
        logger.info(f"Retrieved {len(log_list)} logs")
        return log_list
    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        raise
