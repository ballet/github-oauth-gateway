import json
from unittest.mock import Mock

import pytest
import requests

from ballet_oauth_gateway.conf import TestConfig
from ballet_oauth_gateway.db import db, Auth


def test_status(client):
    response = client.get('/status')
    assert response.status_code == 200
    assert b'OK' in response.data


def test_app_id(client):
    response = client.get('/api/app_id')
    assert response.status_code == 200
    assert TestConfig.CLIENT_ID in response.data.decode()


def test_authorize(client):
    code = 'foo'
    state = 'bar'
    response = client.get(f'/api/authorize?code={code}&state={state}')
    assert response.status_code == 200
    assert b'OK' in response.data

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

    response = client.post('/api/access_token', data={'state': state})
    data = json.loads(response.data)

    assert data['access_token'] == token
    assert Auth.query.filter_by(state=state).count() == 0


def test_success(client):
    response = client.get('/success')
    assert response.status_code == 200
