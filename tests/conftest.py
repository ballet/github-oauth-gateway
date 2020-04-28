import pytest

from ballet_oauth_gateway import create_app


@pytest.fixture
def app():
    app = create_app(testing=True)
    app.config['TESTING'] = True
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()
