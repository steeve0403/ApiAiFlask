from src import db, bcrypt
from datetime import datetime


class User(db.Model):
    """
    User model to store user information.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Role can be 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, firstname, lastname, email, password, role='user'):
        """
        Initialize the user with hashed password and role.
        """
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

    def verify_password(self, password):
        """
        Verify the password with the hashed value.
        """
        return bcrypt.check_password_hash(self.password, password)

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
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.role}')"
