import requests

GITHUB_OAUTH_URL = 'https://github.com/login/oauth/access_token'


def request_token(client_id, client_secret, code, redirect_uri, state):
    url = GITHUB_OAUTH_URL

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'state': state,
    }

    headers = {
        'Accept': 'application/json'
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()

    return response.json()
