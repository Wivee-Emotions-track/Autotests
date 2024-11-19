import pytest

from api.shops_api.shops_api import ShopsApi


@pytest.fixture()
def fixture_shops_api():
    return ShopsApi()
