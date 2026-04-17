import pytest

from PixieDust.app import PixieDust


@pytest.fixture
def app():
    return PixieDust()
