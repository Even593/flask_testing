import re

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message": "Request body must be JSON"}), 400

    errors = {}

    username = data.get('username', '').strip()
    if not username:
        errors['username'] = 'Username is required'
    elif len(username) < 3 or len(username) > 80:
        errors['username'] = 'Username must be between 3 and 80 characters'
    elif not re.match(r'^\w+$', username):
        errors['username'] = 'Username must contain only letters, numbers, and underscores'

    email = data.get('email', '').strip()
    if not email:
        errors['email'] = 'Email is required'
    elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        errors['email'] = 'Invalid email format'

    password = data.get('password', '')
    if not password:
        errors['password'] = 'Password is required'
    elif len(password) < 8:
        errors['password'] = 'Password must be at least 8 characters'

    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Conflict", "message": "Username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Conflict", "message": "Email already exists"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message": "Request body must be JSON"}), 400

    errors = {}

    username = data.get('username', '').strip()
    if not username:
        errors['username'] = 'Username is required'

    password = data.get('password', '')
    if not password:
        errors['password'] = 'Password is required'

    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Unauthorized", "message": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Forbidden", "message": "Account is disabled"}), 403

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {"id": user.id, "username": user.username}
    }), 200
