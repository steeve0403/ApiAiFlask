from src import db
from datetime import datetime
import logging

# Logger configuration
logger = logging.getLogger(__name__)

class Log(db.Model):
    """
    Model for storing user activity logs.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, action):
        """
        Initialize a log entry with the user ID and action.

        :param user_id: ID of the user who performed the action.
        :param action: Description of the action performed.
        """
        self.user_id = user_id
        self.action = action

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

