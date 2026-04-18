from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select

from app import db
from app.models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Not Found", "message": f"User with id {user_id} not found"}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({"error": "Unauthorized", "message": "User not found"}), 401
    return jsonify(user.to_dict()), 200
