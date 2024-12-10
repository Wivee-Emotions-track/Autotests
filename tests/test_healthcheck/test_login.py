from time import sleep

import allure
import pytest

from ui.pages.dashboard_page import DashboardPage
from ui.pages.login_page import LoginPage
from configs.config import get_env_configs, get_env


correct_login = get_env_configs(get_env())['credentials']['admin']['login']
correct_password = get_env_configs(get_env())['credentials']['admin']['password']


@pytest.mark.parametrize("username, password, valid", [
    (correct_login, correct_password, True)
])
@allure.title("Check login with valid/invalid username and password")
def test_wayvee_login(page, get_config, username, password, valid):

    login_page = LoginPage(page, get_config['urls']['host'])
    login_page.open('https://app.wayvee.com/')
    # login_page.open()

    login_page.login(username, password)
    sleep(5)
    dashboard_page = DashboardPage(page)
    dashboard_page.check_logged_in()
