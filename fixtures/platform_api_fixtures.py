import pytest

from api.shops_api.shops_api import ShopsApi
from api.shops_api.users_api import UsersApi
from api.token_api.token_api_actions import TokenApiActions


@pytest.fixture()
def fixture_shops_api():
    return ShopsApi()


@pytest.fixture()
def fixture_token_api():
    return TokenApiActions()

@pytest.fixture()
def fixture_users_api():
    return UsersApi()
