import pytest

from gudlft.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
