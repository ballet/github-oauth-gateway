from ballet_oauth_gateway import db
from ballet_oauth_gateway.conf import TestConfig
from ballet_oauth_gateway.models import Auth


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


def test_access_token(client, monkeypatch):
    # prepare entry in db
    code = 'foo'
    state = 'bar'
    auth = Auth(code=code, state=state)
    db.session.add(auth)
    db.session.commit()

    # mock response to request token
    # TODO

    assert True



def test_success(client):
    response = client.get('/success')
    assert response.status_code == 200
