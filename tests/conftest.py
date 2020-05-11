import tempfile

import pytest

from github_oauth_gateway import create_app
from github_oauth_gateway.conf import Config


@pytest.fixture
def app(monkeypatch):
    db_fd, db_path = tempfile.mkstemp()
    monkeypatch.setattr(Config, 'SQLALCHEMY_DATABASE_URI', f'sqlite:///{db_path}')

    app = create_app(testing=True)
    app.config['TESTING'] = True
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()
