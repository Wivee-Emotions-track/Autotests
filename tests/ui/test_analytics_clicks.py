import allure
import pytest
from ui.pages.login_page import LoginPage
from ui.pages.analytics_page import AnalyticsPage

@pytest.fixture(scope="function")
def setup(page):
    username = "testing_admin@wayvee.com"
    password = "kz767ErQ9DvNXHuo1afB"
    login_page = LoginPage(page)
    analytics_page = AnalyticsPage(page)
    login_page.open()
    login_page.login(username, password)
    yield analytics_page

@allure.title("Test table preview")
def test_table_check(page, setup):
    analytics_page = setup

    with allure.step("Click to Table button"):
        try:
            analytics_page.click_table()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e

    with allure.step("Click to Edit table button"):
        try:
            analytics_page.click_edit_table()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e

    with allure.step("Click to Edit table button again to close it"):
        try:
            analytics_page.click_edit_table()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e

    with allure.step("Click to the Export button"):
        try:
            analytics_page.click_export()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e

    with allure.step("Fill the File Name and click to download button"):
        try:
            analytics_page.click_download()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e

@allure.title("Test line_chart preview")
def test_graph_check(page, setup):
    analytics_page = setup

    with allure.step("Click to Line-charted button"):
        try:
            analytics_page.click_graphics()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e

    with allure.step("Click to Table button"):
        try:
            analytics_page.click_table()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e

    with allure.step("Click to Line-charted button"):
        try:
            analytics_page.click_graphics()
        except Exception as e:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e