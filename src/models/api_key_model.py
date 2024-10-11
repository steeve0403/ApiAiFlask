import uuid
from src import db
import logging
from datetime import datetime, timezone

# Logger configuration
logger = logging.getLogger(__name__)


class ApiKeyModel(db.Model):
    """
    Model for storing API keys associated with users.
    """
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, user_id):
        """
        Initialize the API key with a unique value and associate it with a user.

        :param user_id: ID of the user who owns the API key.
        """
        self.key = str(uuid.uuid4())  # Generate a unique API key
        self.user_id = user_id

    def save(self):
        """
        Save the API key to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"API key {self.key} created for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error saving API key: {str(e)}")
            db.session.rollback()

    @classmethod
    def find_by_key(cls, key):
        """
        Find an API key by its value.

        :param key: The API key to find.
        :return: The ApiKeyModel instance if found, None otherwise.
        """
        try:
            return cls.query.filter_by(key=key).first()
        except Exception as e:
            logger.error(f"Error finding API key: {str(e)}")
            return None
