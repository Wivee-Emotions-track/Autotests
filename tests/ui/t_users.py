import time
from datetime import datetime
from os import path

import allure
import pytest

from ui.pages.analytics_page import AnalyticsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.invite_user_page import InviteUserPage
from ui.pages.login_page import LoginPage
from ui.pages.users_page import UsersPage


@pytest.fixture()
def create_user(fixture_users_api):
    user_email = "tira-tore@yandex.ru"
    user_id = fixture_users_api.create_user(user_email, "Qwerty_0000")
    yield user_email


@allure.title("Test add user")
def test_add_user(page, login, get_config):
    user_mail = "testmail@gmail.com"
    password = "Qwerty_0000"
    users_page = UsersPage(page)
    time.sleep(5)  # todo
    users_page.add_user()

    invite_user_page = InviteUserPage(page)
    invite_user_page.invite_user(user_mail)
    # todo
    invite_user_page.set_password(password)
    invite_user_page.go_to_sigh_in_page()

    login_page = LoginPage(page, get_config['urls']['host'])
    login_page.login(user_mail, password)

    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()


@allure.title("Test delete user")
def test_delete_user(page, create_user, login):
    user_email = create_user
    sidebar = DashboardPage(page)
    sidebar.open_users_page('Users', sidebar.users)

    users_page = UsersPage(page)
    users_page.search_user(user_email)
    users_page.delete_user(user_email)
    users_page.search_user(user_email, False)
