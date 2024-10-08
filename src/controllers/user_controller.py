import os
from datetime import datetime
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
from src import db
from src.models.token_model import RevokedToken
from src.models.user_model import User
from src.models.api_key_model import ApiKeyModel


def generate_api_key():
    current_user_id = get_jwt_identity()
    new_api_key = ApiKeyModel(user_id=current_user_id)
    new_api_key.save()
    return jsonify({'api-key': new_api_key.key}), 201


def signup():
    try:
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')

        if not firstname or not lastname or not email or not password:
            return jsonify({'status': "failed", "message": "Missing parameters"}), 400

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'status': "failed", "message": "User already exists"}), 409

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
        access_token = create_access_token(identity={'user_id': new_user.id, 'role': new_user.role})
        return jsonify({'status': "success", "message": "User Sign up Successful", "access_token": access_token}), 201

    except Exception as e:
        return jsonify({'status': "failed", "message": "An error occurred", "error": str(e)}), 500


def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'status': "failed", "message": "Email and Password are required"}), 400

        # Vérifier l'utilisateur dans la base de données
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'status': "failed", "message": "User not found"}), 404

        # Vérifier le mot de passe
        if not check_password_hash(user.password, password):
            return jsonify({'status': "failed", "message": "Invalid Password"}), 401

        # Si le mot de passe est correct, générer un token JWT
        access_token = create_access_token(identity={'user_id': user.id, 'role': user.role})
        return jsonify({'status': "success", "message": "User Login Successful", "access_token": access_token}), 200

    except Exception as e:
        return jsonify({'status': "failed", "message": "An error occurred", "error": str(e)}), 500

@jwt_required()
def logout():
    jti = get_jwt()['jti'] # JWT ID
    revoked_token = RevokedToken(jti=jti)
    revoked_token.add()
    return jsonify({"message": "Successfully logged out"}), 200
