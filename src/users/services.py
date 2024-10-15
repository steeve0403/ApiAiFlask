from src import db
from src.exceptions import ConflictError, ValidationError, NotFoundError
from src.extensions import bcrypt
import logging

from src.tokens.services import create_jwt_token
from src.users.models import User

# Logger configuration
logger = logging.getLogger(__name__)


def signup_user(data, role='user'):
    """
    Sign up a new user by creating a new account.
    :param data: Dictionary containing user details.
    :param role: Role of the user (default is 'user').
    :return: Tokens if signup is successful.
    """
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')

    if not firstname or not lastname or not email or not password:
        raise ValidationError("Missing parameters")

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise ConflictError("User already exists")

    # Create new user and hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=hashed_password,
        role=role  # Set the role of the user
    )

    db.session.add(new_user)
    db.session.commit()

    # Generate a JWT token for the new user
    tokens = create_jwt_token(user_id=new_user.id, role=new_user.role)
    logger.info(f"New user signed up: {email}")
    return tokens


def login_user(data):
    """
    Log in an existing user by verifying their credentials.

    :param data: Dictionary containing login details.
    :return: Tokens if login is successful.
    """
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise ValidationError("Email and Password are required")

    # Check user in database
    user = User.query.filter_by(email=email).first()
    if not user:
        logger.warning(f"Login failed: User with email {email} not found")
        raise NotFoundError("User not found")

    # Verify password
    password = data.get('password')
    password_valid = user.verify_password(password)
    if not password_valid:
        # Log the password hash and the provided password
        logger.debug(f"Stored password hash for user {email}: {user.password_hash}")
        logger.debug(f"Password provided by user: {password}")
        raise ValidationError("Invalid Password")

    # If the password is correct, generate a JWT token
    tokens = create_jwt_token(user_id=user.id, role=user.role)
    logger.info(f"User logged in: {email}")
    return tokens
