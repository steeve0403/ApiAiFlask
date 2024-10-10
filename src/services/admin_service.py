from src.models.user_model import User
from src import db
import logging

# Logger configuration
logger = logging.getLogger(__name__)

def get_dashboard_stats():
    """
    Retrieve statistics for the admin dashboard.

    :return: Dictionary containing statistics.
    """
    try:
        total_users = User.query.count()
        statistics = {
            "total_users": total_users,
            "total_active_users": User.query.filter_by(is_active=True).count(),
            "total_inactive_users": User.query.filter_by(is_active=False).count(),
            "total_admins": User.query.filter_by(role='admin').count(),
            "total_users_with_api_keys": User.query.filter(User.api_key != None).count()
        }
        return statistics
    except Exception as e:
        logger.error(f"Error retrieving dashboard statistics: {str(e)}")
        raise

def get_all_users():
    """
    Retrieve a list of all users.

    :return: List of user objects.
    """
    try:
        users = User.query.all()
        return users
    except Exception as e:
        logger.error(f"Error retrieving all users: {str(e)}")
        raise

def change_user_role(user_id, new_role):
    """
    Change the role of a user.

    :param user_id: ID of the user.
    :param new_role: New role to assign to the user.
    :return: User object after modification or None if user not found.
    """
    try:
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            logger.info(f"User role changed: {user.email} is now an {new_role}")
            return user
        else:
            return False
    except Exception as e:
        logger.error(f"Error changing user role: {str(e)}")
        raise