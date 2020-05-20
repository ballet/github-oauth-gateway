import json
from unittest.mock import Mock

import pytest
import requests

from github_oauth_gateway.conf import TestConfig
from github_oauth_gateway.db import db, Auth

PREFIX = '/api/v1'


def test_app_id(client):
    response = client.get(PREFIX + '/app_id')
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert 'client_id' in response_json
    assert TestConfig.CLIENT_ID == response_json['client_id']


def test_authorize(client):
    code = 'foo'
    state = 'bar'

    response = client.get(PREFIX + f'/authorize?code={code}&state={state}', follow_redirects=True)

    # should have a generic success page
    assert response.status_code == 200
    assert 'doctype html' in response.data.decode().lower()
    assert 'success' in response.data.decode().lower()

    auths = Auth.query.all()
    assert len(auths) == 1

    auth = Auth.query.filter_by(state=state).one()
    assert auth.code == code
    assert auth.state == state


@pytest.fixture
def mock_access_token(monkeypatch):
    data = {
        "access_token": "123",
        "scope": "repo,gist",
        "token_type": "bearer"
    }

    # mock response to request token
    mock_response = Mock(autospec=requests.Response)
    mock_response.json.return_value = data

    def mock_post(*args, **kwargs):
        return mock_response

    monkeypatch.setattr(requests, 'post', mock_post)

    return data


def test_access_token(client, mock_access_token):
    # prepare entry in db
    code = 'foo'
    state = 'bar'
    token = 'baz'
    mock_access_token['access_token'] = token

    auth = Auth(code=code, state=state)
    db.session.add(auth)
    db.session.commit()

    response = client.post(PREFIX + '/access_token', json={'state': state})
    data = json.loads(response.data)

    assert data['access_token'] == token
    assert Auth.query.filter_by(state=state).count() == 0


def test_access_token_no_code(client, socket_disabled):
    state = 'nonexistent'
    response = client.post(PREFIX + '/access_token', json={'state': state})
    assert response.status_code == 400
    data = json.loads(response.data)
    message = data['message']
    assert 'no authorization code' in message.lower()


def test_success(client):
    response = client.get(PREFIX + '/success')
    assert response.status_code == 200
