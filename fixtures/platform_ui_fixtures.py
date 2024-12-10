import pytest

from ui.pages.login_page import LoginPage


@pytest.fixture(scope="function")
def login(page, get_config):
    username = get_config['credentials']['super_user']['login']
    password = get_config['credentials']['super_user']['password']

    login_page = LoginPage(page, get_config['urls']['host'])
    login_page.open()
    login_page.login(username, password)
    page.wait_for_url("**/analytics?zones=&shops=", wait_until="load", timeout=20000)

