import time
from datetime import datetime

import allure

from api.external_api.external_api import ExternalApi
from ui.pages.api_tokens_page import TokensPage
from ui.pages.dashboard_page import DashboardPage


@allure.title("Test add token")
def test_add_token(page, login):
    token_name = f'AutotestToken_{datetime.utcnow().strftime("%d_%m_%H_%M")}'

    sidebar = DashboardPage(page)
    sidebar.open_api_page()

    token_page = TokensPage(page)
    time.sleep(2)  # todo
    token_page.add_token(token_name)
    token = token_page.get_created_token(token_name)

    ext_api = ExternalApi()
    ext_api.get_shops_list(token)


@allure.title("Test revoke token")
def test_revoke_token(page, login):
    token_name = f'AutotestToken_{datetime.utcnow().strftime("%d_%m_%H_%M")}'

    sidebar = DashboardPage(page)
    sidebar.open_api_page()

    token_page = TokensPage(page)
    time.sleep(2)  # todo
    token_page.add_token(token_name)
    token = token_page.get_created_token(token_name)

    token_page.revoke_token(token_name)

    ext_api = ExternalApi()
    response = ext_api.get_shops_list(token, check_response=False)
    assert not response.ok, 'Token is not revoked'
