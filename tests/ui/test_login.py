from time import sleep

import allure
import pytest
from allure import step
from ui.pages.login_page import LoginPage


@pytest.mark.parametrize("username, password, valid", [
    ("testing_admin@wayvee.com", 'kz767ErQ9DvNXHuo1afB', True),
])
@allure.title("Check login with valid/invalid username and password")
def test_wayvee_login(page, username, password, valid):

    login_page = LoginPage(page)
    login_page.open()

    login_page.login(username, password)
    sleep(5)

    login_page.check_logged_in()