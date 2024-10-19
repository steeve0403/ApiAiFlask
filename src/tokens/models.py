from src.extensions import db
from datetime import datetime, timezone
import logging

# Logger configuration
logger = logging.getLogger(__name__)

class RevokedToken(db.Model):
    """
    Model for storing revoked JWT tokens to prevent reuse.
    """
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)  # JWT ID with indexing for faster lookup
    revoked_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def add(self):
        """
        Add the revoked token to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"Token {self.jti} revoked at {self.revoked_at}")
        except Exception as e:
            logger.error(f"Error adding revoked token: {str(e)}")
            db.session.rollback()

    @classmethod
    def is_token_revoked(cls, jti):
        """
        Check if a JWT token has been revoked.

        :param jti: The JTI (unique identifier) of the token to check.
        :return: True if the token is revoked, False otherwise.
        """
        try:
            query = cls.query.filter_by(jti=jti).first()
            return bool(query)
        except Exception as e:
            logger.error(f"Error checking if token is revoked: {str(e)}")
            return False

    @classmethod
    def clean_revoked_tokens(cls):
        """
        Remove tokens that were revoked more than 7 days ago (assuming the token expiration).
        This can be called periodically as a maintenance task.
        """
        try:
            expired_time = datetime.now(timezone.utc) - timedelta(days=7)
            cls.query.filter(cls.revoked_at < expired_time).delete()
            db.session.commit()
            logger.info("Old revoked tokens cleaned up.")
        except Exception as e:
            logger.error(f"Error cleaning up revoked tokens: {str(e)}")
            db.session.rollback()