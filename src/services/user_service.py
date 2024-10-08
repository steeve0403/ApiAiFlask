from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user_model import User
from src import db
from src.services.jwt_service import create_jwt_token
import logging

# Logger configuration
logger = logging.getLogger(__name__)


def signup_user(data):
    """
    Sign up a new user by creating a new account.

    :param data: Dictionary containing user details.
    :return: Tokens if signup is successful.
    """
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')

    if not firstname or not lastname or not email or not password:
        raise ValueError("Missing parameters")

    # Vérifier si l'utilisateur existe déjà
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise ValueError("User already exists")

    # Créer un nouvel utilisateur et hacher le mot de passe
    hashed_password = generate_password_hash(password)
    new_user = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=hashed_password,
        role='user'  # Par défaut, chaque nouvel utilisateur est un simple utilisateur
    )

    db.session.add(new_user)
    db.session.commit()

    # Générer un token JWT pour le nouvel utilisateur
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
        raise ValueError("Email and Password are required")

    # Vérifier l'utilisateur dans la base de données
    user = User.query.filter_by(email=email).first()
    if not user:
        raise ValueError("User not found")

    # Vérifier le mot de passe
    if not check_password_hash(user.password, password):
        raise ValueError("Invalid Password")

    # Si le mot de passe est correct, générer un token JWT
    tokens = create_jwt_token(user_id=user.id, role=user.role)
    logger.info(f"User logged in: {email}")
    return tokens
