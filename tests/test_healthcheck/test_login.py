from time import sleep

import allure
import pytest

from ui.pages.dashboard_page import DashboardPage
from ui.pages.login_page import LoginPage
from configs.config import get_env_configs, get_env


@pytest.mark.parametrize("valid", [True, False])
@allure.title("Check login with valid/invalid username and password")
def test_wayvee_login(page, get_config, valid):
    login_page = LoginPage(page, get_config['urls']['host'])

    login_page.open()
    if valid:
        username = get_config['credentials']['super_user']['login']
        password = get_config['credentials']['super_user']['password']
    else:
        username = get_config['credentials']['super_user']['login']
        password = 'incorrect_password'

    login_page.login(username, password)
    sleep(5)
    if valid:
        dashboard_page = DashboardPage(page)
        dashboard_page.check_logged_in()
    else:
        login_page.check_error_msg()
