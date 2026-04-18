import time
import pytest


class TestGetUser:
    def test_get_user_found(self, seeded_client):
        resp = seeded_client.get('/api/user/1')
        assert resp.status_code == 200
        assert resp.json['username'] == 'testuser'

    def test_get_user_not_found(self, seeded_client):
        resp = seeded_client.get('/api/user/999')
        assert resp.status_code == 404

    def test_get_user_string_id(self, client):
        resp = client.get('/api/user/abc')
        assert resp.status_code == 404


class TestGetProfile:
    def test_profile_with_valid_token(self, seeded_client, auth_headers):
        resp = seeded_client.get('/api/profile', headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json['username'] == 'testuser'

    def test_profile_without_token(self, seeded_client):
        resp = seeded_client.get('/api/profile')
        assert resp.status_code == 401
        assert 'Missing' in resp.json['message']

    def test_profile_with_invalid_token(self, seeded_client):
        resp = seeded_client.get('/api/profile', headers={
            'Authorization': 'Bearer invalid.token.here'
        })
        assert resp.status_code == 401

    def test_profile_with_expired_token(self, seeded_app, seeded_client):
        with seeded_app.app_context():
            resp = seeded_client.post('/api/login', json={
                'username': 'testuser', 'password': 'Testpass1!'
            })
            token = resp.json['access_token']

        time.sleep(2)

        resp = seeded_client.get('/api/profile', headers={
            'Authorization': f'Bearer {token}'
        })
        assert resp.status_code == 401
        assert 'expired' in resp.json['message'].lower()
