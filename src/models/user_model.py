import logging

from src import db, bcrypt
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class User(db.Model):
    """
    User model to store user information.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Role can be 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=False)
    api_keys = db.relationship('ApiKeyModel', backref='user', lazy='dynamic')

    def __init__(self, firstname, lastname, email, password, role='user'):
        """
        Initialize the user with hashed password and role.
        """
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = password
        self.role = role

    def verify_password(self, password):
        """
        Verify the password with the hashed value.
        """
        result = bcrypt.check_password_hash(self.password_hash, password)
        logger.debug(f"Password verification result: {result}")
        return result

    def save(self):
        """
        Save the user to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the user from the database.
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.role}', '{self.is_active}')"
