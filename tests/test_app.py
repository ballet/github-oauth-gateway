from ballet_oauth_gateway.conf import TestConfig


def test_status(client):
    response = client.get('/status')
    assert response.status_code == 200
    assert b'OK' in response.data

def test_app_id(client):
    response = client.get('/app_id')
    assert response.status_code == 200
    assert TestConfig.CLIENT_ID in response.data.decode()
