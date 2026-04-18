from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from app.config import config_by_name

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name='dev'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    jwt.init_app(app)

    _register_jwt_error_callbacks(jwt)

    from app.routes import register_blueprints
    register_blueprints(app)

    from app.errors import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        from app.models import User  # noqa: F401
        db.create_all()

    return app


def _register_jwt_error_callbacks(jwt_manager):
    @jwt_manager.unauthorized_loader
    def missing_token(callback):
        return jsonify({"error": "Unauthorized", "message": "Missing Authorization Header"}), 401

    @jwt_manager.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify({"error": "Unauthorized", "message": "Token has expired"}), 401

    @jwt_manager.invalid_token_loader
    def invalid_token(callback):
        return jsonify({"error": "Unauthorized", "message": "Invalid token"}), 401
