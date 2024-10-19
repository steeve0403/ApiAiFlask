import logging
from src.extensions import db
from datetime import datetime, timezone, timedelta

# Logger configuration
logger = logging.getLogger(__name__)


class Log(db.Model):
    """
    Model for storing user activity logs.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # For storing IPv4/IPv6 addresses

    def __init__(self, user_id, action, details=None, ip_address=None):
        """
        Initialize a log entry with the user ID, action, and optional details.
        :param user_id: ID of the user who performed the action.
        :param action: Description of the action performed.
        :param details: Additional details about the action (optional).
        :param ip_address: IP address from where the action was performed (optional).
        """
        self.user_id = user_id
        self.action = action
        self.details = details
        self.ip_address = ip_address

    def save(self):
        """
        Save the log entry to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"Log entry added for user {self.user_id}: {self.action}")
        except Exception as e:
            logger.error(f"Error saving log entry: {str(e)}")
            db.session.rollback()

    @classmethod
    def find_by_user_id(cls, user_id):
        """
        Find all log entries by user ID.
        :param user_id: The user ID to search for.
        :return: List of log entries for the user.
        """
        try:
            return cls.query.filter_by(user_id=user_id).all()
        except Exception as e:
            logger.error(f"Error finding logs for user {user_id}: {str(e)}")
            return []

    @classmethod
    def find_by_user_id_paginated(cls, user_id, page, per_page):
        """
        Find paginated log entries by user ID.
        :param user_id: The user ID to search for.
        :param page: The page number.
        :param per_page: The number of logs per page.
        :return: Paginated list of log entries for the user.
        """
        try:
            return cls.query.filter_by(user_id=user_id).paginate(page, per_page, error_out=False)
        except Exception as e:
            logger.error(f"Error finding paginated logs for user {user_id}: {str(e)}")
            return []

    @classmethod
    def find_by_action(cls, action):
        """
        Find all log entries by action.
        :param action: The action to search for.
        :return: List of log entries with the specified action.
        """
        try:
            return cls.query.filter_by(action=action).all()
        except Exception as e:
            logger.error(f"Error finding logs for action '{action}': {str(e)}")
            return []

    @classmethod
    def find_by_date_range(cls, start_date, end_date):
        """
        Find all log entries within a specific date range.
        :param start_date: The start date of the range.
        :param end_date: The end date of the range.
        :return: List of log entries within the specified date range.
        """
        try:
            return cls.query.filter(cls.timestamp >= start_date, cls.timestamp <= end_date).all()
        except Exception as e:
            logger.error(f"Error finding logs between {start_date} and {end_date}: {str(e)}")
            return []

    @classmethod
    def delete_old_logs(cls, older_than_days):
        """
        Delete log entries older than a specified number of days.
        :param older_than_days: Number of days before which logs should be deleted.
        """
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=older_than_days)
            cls.query.filter(cls.timestamp < cutoff_date).delete()
            db.session.commit()
            logger.info(f"Old logs older than {older_than_days} days deleted.")
        except Exception as e:
            logger.error(f"Error deleting old logs: {str(e)}")
            db.session.rollback()

    def delete(self):
        """
        Delete the log entry from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info(f"Log entry deleted for user {self.user_id}: {self.action}")
        except Exception as e:
            logger.error(f"Error deleting log entry: {str(e)}")
            db.session.rollback()

    def __repr__(self):
        return f"Log(user_id={self.user_id}, action='{self.action}', timestamp={self.timestamp}, details='{self.details}', ip_address='{self.ip_address}')"
