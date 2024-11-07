from datetime import datetime

import allure
import pytest
from ui.pages.login_page import LoginPage
from ui.pages.analytics_page import AnalyticsPage


@pytest.fixture(scope="function")
def setup(page):
    username = "testing_admin@wayvee.com"
    password = "kz767ErQ9DvNXHuo1afB"
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)


@allure.title("Test table preview")
def test_table_check(page, setup):
    file_name = f'AutotestExport_{datetime.utcnow().strftime("%d_%m_%H_%M")}'
    analytics_page = AnalyticsPage(page)
    analytics_page.open_graphics()
    analytics_page.open_table()
    analytics_page.open_settings()
    analytics_page.export_data(file_name)
