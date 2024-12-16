import time

import allure

from ui.pages.alert_page import AlertPage
from ui.pages.alert_rules import AlertRules
from ui.pages.analytics_page import AnalyticsPage
from ui.pages.api_tokens_page import TokensPage
from ui.pages.calibration_page import CalibrationPage
from ui.pages.devices_page import DevicesPage
from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.manufactured_page import ManufacturedPage
from ui.pages.shops_page import ShopsPage
from ui.pages.users_page import UsersPage
from ui.pages.video_markup_page import VideoMarkupPage


@allure.title("Test dashboard pages")
def test_dashboard_pages(page, login):

    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.check_loader_absence()
    time.sleep(5) # todo
    shops_page.check_page_opened()

    sidebar.open_analytics_page()
    analytics_page = AnalyticsPage(page)
    analytics_page.check_page_opened()

    sidebar.open_api_page()
    token_page = TokensPage(page)
    time.sleep(5) # todo
    token_page.check_page_opened()

    with allure.step("Go to alert messages"):
        sidebar.open_alerts_page('Alert Messages', sidebar.alert_msg)
        AlertPage(page).check_page_opened()

    with allure.step("Go to alert rules"):
        sidebar.open_alerts_page('Alert Rules', sidebar.alert_rules)
        AlertRules(page).check_page_opened()


@allure.title("Test dashboard users pages")
def test_dashboard_users_pages(page, login):

    sidebar = DashboardPage(page)
    sidebar.open_shops_page()
    shops_page = ShopsPage(page)
    shops_page.check_loader_absence()
    time.sleep(5) # todo
    shops_page.check_page_opened()

    with allure.step("Go to users"):
        sidebar.open_users_page('Users', sidebar.users)
        UsersPage(page).check_page_opened()
        
    with allure.step("Go to Devices"):
        sidebar.open_users_page('Devices', sidebar.devices)
        devices_page = DevicesPage(page)
        time.sleep(5) # todo
        devices_page.check_page_opened()

    with allure.step("Go to Manufactured"):
        sidebar.open_users_page('Manufactured', sidebar.manufactured)
        manufactured_page = ManufacturedPage(page)
        time.sleep(5) # todo
        manufactured_page.check_page_opened()
        manufactured_page.check_table_is_not_empty()

    with allure.step("Go to Calibration"):
        sidebar.open_users_page('Calibration', sidebar.calibration)
        calibration_page = CalibrationPage(page)
        time.sleep(5) # todo
        calibration_page.check_page_opened()

    with allure.step("Go to Video Markup"):
        sidebar.open_users_page('Video Markup', sidebar.video_markup)
        video_markup_page = VideoMarkupPage(page)
        time.sleep(5) # todo
        video_markup_page.check_page_opened()
        video_markup_page.check_page_is_not_empty()
