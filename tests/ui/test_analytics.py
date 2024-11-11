from datetime import datetime

import allure
import pytest
from ui.pages.login_page import LoginPage
from ui.pages.analytics_page import AnalyticsPage


@pytest.fixture(scope="function")
def login(page):
    username = "dmitrijdmtirij@gmail.com"
    password = "Qwerty_0000"

    login_page = LoginPage(page)
    url_with_date_filters = login_page.url + '/analytics?zones=&shops=&from=2024-08-13&to=2024-11-11'
    login_page.open(url_with_date_filters)
    login_page.login(username, password)


@allure.title("Test table preview")
def test_table_check(page, login):
    file_name = f'AutotestExport_{datetime.utcnow().strftime("%d_%m_%H_%M")}'
    analytics_page = AnalyticsPage(page)
    analytics_page.open_graphics()
    analytics_page.open_table()
    analytics_page.open_settings()
    analytics_page.export_data(file_name)


@allure.title("Test edit table columns")
def test_edit_table_columns(page, login):
    analytics_page = AnalyticsPage(page)
    analytics_page.open_settings()

    with allure.step("Hide columns"):
        analytics_page.switch_menu_column('Avg. Dwell Time')
        analytics_page.switch_menu_column('Dwell Number')
        analytics_page.switch_menu_column('Engagements Number')
        analytics_page.switch_menu_column('Avg. Engagements per Customer')
        analytics_page.switch_menu_column('Avg. Speed')
        analytics_page.switch_menu_column('C-SAT')
        analytics_page.switch_menu_column('Bypassers Number')

    analytics_page.save_settings()

    analytics_page.check_column_presence('Avg. Dwell Time')
    analytics_page.check_column_presence('Dwell Number')
    analytics_page.check_column_presence('Engagements Number')
    analytics_page.check_column_presence('Avg. Engagements per Customer')
    analytics_page.check_column_presence('Avg. Speed')
    analytics_page.check_column_presence('C-SAT')
    analytics_page.check_column_presence('Bypassers Number')


@allure.title("Test check filters")
def test_edit_table_columns(page, login):
    analytics_page = AnalyticsPage(page)
    analytics_page.select_comparison('Preceding Period')
    analytics_page.click(analytics_page.table_btn)  # to close drop down menu

    analytics_page.check_comparison_module_is_active()
