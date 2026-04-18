import pytest

from app import create_app, db


@pytest.fixture
def app():
    app = create_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seeded_app(app):
    from app.seed import seed_db
    seed_db(app)
    return app


@pytest.fixture
def seeded_client(seeded_app):
    return seeded_app.test_client()


@pytest.fixture
def auth_token(seeded_client):
    resp = seeded_client.post('/api/login', json={
        'username': 'testuser', 'password': 'Testpass1!'
    })
    return resp.json['access_token']


@pytest.fixture
def auth_headers(auth_token):
    return {'Authorization': f'Bearer {auth_token}'}
