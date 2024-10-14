import uuid
from src import db
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import ValidationError

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
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, valid_for_days=30):
        """
        Initialize the API key with a unique value, associate it with a user, and set the expiration date.

        :param user_id: ID of the user who owns the API key.
        :param valid_for_days: Number of days for which the API key will be valid (default: 30 days).
        """
        self.key = str(uuid.uuid4())  # Generate a unique API key
        self.user_id = user_id
        self.created_at = datetime.now(timezone.utc)
        self.expires_at = self.created_at + timedelta(days=valid_for_days)

    def save(self):
        """
        Save the API key to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"API key {self.key} created for user {self.user_id}, expires at {self.expires_at}")
        except SQLAlchemyError as e:
            logger.error(f"Error saving API key: {str(e)}")
            db.session.rollback()
            raise ValidationError("Failed to save API key.")

    def delete(self):
        """
        Delete the API key from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info(f"API key {self.key} deleted for user {self.user_id}")
        except SQLAlchemyError as e:
            logger.error(f"Error deleting API key: {str(e)}")
            db.session.rollback()
            raise ValidationError("Failed to delete API key.")

    def is_expired(self):
        """
        Check if the API key is expired.
        :return: True if the API key is expired, False otherwise.
        """
        return datetime.now(timezone.utc) > self.expires_at

    @classmethod
    def find_by_key(cls, key):
        """
        Find an API key by its value.
        :param key: The API key to find.
        :return: The ApiKeyModel instance if found, None otherwise.
        """
        try:
            api_key = cls.query.filter_by(key=key).first()
            if api_key and not api_key.is_expired():
                return api_key
            logger.warning(f"API key {key} is expired or does not exist.")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error finding API key: {str(e)}")
            return None

    @classmethod
    def find_by_user_id(cls, user_id):
        """
        Find all valid API keys associated with a given user ID.
        :param user_id: The user ID to find API keys for.
        :return: List of valid ApiKeyModel instances.
        """
        try:
            return cls.query.filter(cls.user_id == user_id, cls.expires_at > datetime.now(timezone.utc)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error finding API keys for user {user_id}: {str(e)}")
            return []

    def __repr__(self):
        return f"ApiKeyModel(key='{self.key}', user_id={self.user_id}, expires_at={self.expires_at})"
