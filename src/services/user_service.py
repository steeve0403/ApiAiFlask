from src.models.user_model import User
from src import db
from src.extensions import bcrypt
from src.services.jwt_service import create_jwt_token
import logging

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
        raise ValueError("Missing parameters")

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise ValueError("User already exists")

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
    logger.info(f"New user signed up: {email}, {password}")
    logger.info(f"Password hash generated: {hashed_password}")
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
        raise ValueError("Email and Password are required")

    # Check user in database
    user = User.query.filter_by(email=email).first()
    if not user:
        raise ValueError("User not found")

    logger.info(f"hash: {user.password}, {password}")
    # Verify password
    if not bcrypt.check_password_hash(user.password, password):
        raise ValueError("Invalid Password")


    # If the password is correct, generate a JWT token
    tokens = create_jwt_token(user_id=user.id, role=user.role)
    logger.info(f"User logged in: {email}")

    # logger.info(f"Stored password hash: {user.password}")
    # logger.info(f"Password provided for verification: {password}")
    #
    # if not bcrypt.check_password_hash(user.password, password):
    #     logger.error("Password verification failed")
    #     raise ValueError("Invalid Password")
    # else:
    #     logger.info("Password verification succeeded")

    return tokens
