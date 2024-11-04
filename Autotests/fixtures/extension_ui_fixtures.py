import pytest

from ui.pages.google_login_page import GoogleLoginPage


@pytest.fixture(scope="function")
def google_login_page(page):
    login_page = GoogleLoginPage(page)
    login_page.open()
    yield login_page
