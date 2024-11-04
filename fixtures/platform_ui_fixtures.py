import pytest

from ui.pages.platform.platform_login_page import PlatformLoginPage


@pytest.fixture(scope="function")
def platform_login_page(page):
    login_page = PlatformLoginPage(page)
    login_page.open()
    yield login_page
