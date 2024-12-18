import time
from datetime import datetime

import allure
import pytest

from api.external_api.external_api import ExternalApi
from ui.pages.api_tokens_page import TokensPage
from ui.pages.dashboard_page import DashboardPage


@pytest.fixture()
def create_token(fixture_token_api):
    token_name = f'AutotestToken_{datetime.utcnow().strftime("%d_%m_%H_%M")}'
    token_id = fixture_token_api.create_token(token_name)
    yield token_name
    fixture_token_api.revoke_token(token_id, check_response=False)


@pytest.fixture()
def find_and_revoke_token(fixture_token_api):
    token_name = f'AutotestToken_{datetime.utcnow().strftime("%d_%m_%H_%M")}'

    yield token_name
    token_id = fixture_token_api.get_token_id_via_name(token_name)
    fixture_token_api.revoke_token(token_id)


@allure.title("Test add token")
def test_add_token(page, login, find_and_revoke_token, get_config):
    token_name = find_and_revoke_token

    sidebar = DashboardPage(page)
    sidebar.open_api_page()

    token_page = TokensPage(page)
    time.sleep(2)  # todo
    token_page.add_token(token_name)
    token = token_page.get_created_token(token_name)

    ext_api = ExternalApi(get_config['urls']['external'])
    ext_api.get_shops_list(token)


@allure.title("Test revoke token")
def test_revoke_token(create_token, page, login, get_config):
    token_name = create_token

    sidebar = DashboardPage(page)
    sidebar.open_api_page()

    token_page = TokensPage(page)
    time.sleep(5)  # todo
    token = token_page.get_created_token(token_name)

    token_page.revoke_token(token_name)

    ext_api = ExternalApi(get_config['urls']['external'])
    response = ext_api.get_shops_list(token, check_response=False)
    assert not response.ok, 'Token is not revoked'
