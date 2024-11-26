import pytest

from ui.pages.login_page import LoginPage


@pytest.fixture(scope="function")
def login(page):
    username = "dmitrijdmtirij@gmail.com"
    password = "Qwerty_0000"

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)
    page.wait_for_url("**/analytics?zones=&shops=", wait_until="load", timeout=10000)

