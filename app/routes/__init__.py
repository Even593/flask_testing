from app.routes.auth import auth_bp
from app.routes.user import user_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
