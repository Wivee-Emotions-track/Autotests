import pytest

from api.devices.device_api_actions import DeviceApiActions
from api.devices.devices_api import DevicesApi
from api.industrial_api.industrial_api import IndustrialApi
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


@pytest.fixture()
def fixture_devices_api():
    return DeviceApiActions()

@pytest.fixture()
def fixture_industrial_api():
    return IndustrialApi()

