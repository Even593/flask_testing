import pytest


class TestRegister:
    def test_register_success(self, client):
        resp = client.post('/api/register', json={
            'username': 'alice', 'email': 'alice@example.com', 'password': 'Password1!'
        })
        assert resp.status_code == 201
        assert resp.json['message'] == 'User created'
        assert resp.json['user']['username'] == 'alice'

    def test_register_missing_username(self, client):
        resp = client.post('/api/register', json={
            'email': 'alice@example.com', 'password': 'Password1!'
        })
        assert resp.status_code == 400
        assert 'username' in resp.json['details']

    def test_register_short_password(self, client):
        resp = client.post('/api/register', json={
            'username': 'alice', 'email': 'alice@example.com', 'password': 'short'
        })
        assert resp.status_code == 400
        assert 'password' in resp.json['details']

    def test_register_invalid_email(self, client):
        resp = client.post('/api/register', json={
            'username': 'alice', 'email': 'not-an-email', 'password': 'Password1!'
        })
        assert resp.status_code == 400
        assert 'email' in resp.json['details']

    def test_register_duplicate_username(self, client):
        client.post('/api/register', json={
            'username': 'alice', 'email': 'alice@example.com', 'password': 'Password1!'
        })
        resp = client.post('/api/register', json={
            'username': 'alice', 'email': 'alice2@example.com', 'password': 'Password1!'
        })
        assert resp.status_code == 409

    def test_register_duplicate_email(self, client):
        client.post('/api/register', json={
            'username': 'alice', 'email': 'alice@example.com', 'password': 'Password1!'
        })
        resp = client.post('/api/register', json={
            'username': 'alice2', 'email': 'alice@example.com', 'password': 'Password1!'
        })
        assert resp.status_code == 409

    def test_register_no_body(self, client):
        resp = client.post('/api/register', content_type='application/json')
        assert resp.status_code == 400


class TestLogin:
    def test_login_success(self, seeded_client):
        resp = seeded_client.post('/api/login', json={
            'username': 'testuser', 'password': 'Testpass1!'
        })
        assert resp.status_code == 200
        assert 'access_token' in resp.json
        assert resp.json['user']['username'] == 'testuser'

    def test_login_wrong_password(self, seeded_client):
        resp = seeded_client.post('/api/login', json={
            'username': 'testuser', 'password': 'wrongpassword'
        })
        assert resp.status_code == 401
        assert resp.json['message'] == 'Invalid credentials'

    def test_login_nonexistent_user(self, seeded_client):
        resp = seeded_client.post('/api/login', json={
            'username': 'ghost', 'password': 'Password1!'
        })
        assert resp.status_code == 401

    def test_login_inactive_user(self, seeded_client):
        resp = seeded_client.post('/api/login', json={
            'username': 'inactive', 'password': 'Testpass1!'
        })
        assert resp.status_code == 403
        assert 'disabled' in resp.json['message'].lower()

    def test_login_missing_fields(self, seeded_client):
        resp = seeded_client.post('/api/login', json={})
        assert resp.status_code == 400
