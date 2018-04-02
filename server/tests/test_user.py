import pytest
from flask import json
import datetime
from models.user import User

class TestUserAPI:
    @pytest.fixture
    def url(self):
        return '/api/user'

    def test_get_all_users_empty(self, get, url):
        r = get(url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data == []

    def test_get_all_users(self, get, url, user):
        r = get(url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data[0]['id'] == user.id
        assert data[0]['username'] == user.username

    def test_create_user_broken_json(self, post, url, json_header):
        data = 'This is a string'
        r = post(url, headers=json_header, data=data)
        data = json.loads(r.data)

        assert r.status_code == 400

    def test_create_user(self, post, url, json_header):
        data = json.dumps(dict(
            username = 'testing name'
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 201

    def test_create_user_duplicate_username(self, post, url, json_header):
        data = json.dumps(dict(
            username = 'duplicate name'
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 201

        data = json.dumps(dict(
            username = 'duplicate name'
        ))
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 400

    def test_create_user_missing_field(self, post, url, json_header):
        data = json.dumps(dict())
        r = post(url, headers=json_header, data=data)

        assert r.status_code == 422

    def test_get_user(self, get, url, user):
        s_url = url + '/' + str(user.id)
        r = get(s_url)
        data = json.loads(r.data)

        assert r.status_code == 200
        assert data['id'] == user.id
        assert data['username'] == user.username

    def test_get_user_nonexistant(self, get, url, user):
        s_url = url + '/' + str(user.id+1)
        r = get(s_url)

        assert r.status_code == 404

    def test_delete_user(self, delete, url, user):
        s_url = url + '/' + str(user.id)
        r = delete(s_url)

        assert r.status_code == 200

    def test_delete_user_nonexistant(self, delete, url, user):
        s_url = url + '/' + str(user.id+1)
        r = delete(s_url)

        assert r.status_code == 404