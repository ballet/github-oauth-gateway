import pytest

from ballet_oauth_gateway import create_app


@pytest.fixture
def client():
    app = create_app(testing=True)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
