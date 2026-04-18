from app import db
from app.models import User


SEED_USERS = [
    {"username": "testuser", "email": "test@example.com", "password": "Testpass1!", "is_active": True},
    {"username": "inactive", "email": "inactive@example.com", "password": "Testpass1!", "is_active": False},
    {"username": "admin", "email": "admin@example.com", "password": "Adminpass1!", "is_active": True},
]


def seed_db(app):
    with app.app_context():
        for user_data in SEED_USERS:
            if User.query.filter_by(username=user_data['username']).first():
                continue
            user = User(username=user_data['username'], email=user_data['email'], is_active=user_data['is_active'])
            user.set_password(user_data['password'])
            db.session.add(user)
        db.session.commit()
