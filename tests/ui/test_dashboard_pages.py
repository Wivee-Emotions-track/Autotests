import allure
from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import Dashboard


@allure.title("Test dashboard pages")
def test_dashboard_pages(page):
    username = "testing_admin@wayvee.com"
    password = "kz767ErQ9DvNXHuo1afB"

    login_page = LoginPage(page)
    sidebar = Dashboard(page)

    login_page.open()
    login_page.login(username, password)

    sidebar.open_shops_page()
    sidebar.open_analytics_page()
    sidebar.open_api_page()

    with allure.step("Go to alert messages"):
        sidebar.open_alerts_page('Alert Messages', sidebar.alert_msg)
    with allure.step("Go to alert rules"):
        sidebar.open_alerts_page('Alert Rules', sidebar.alert_rules)

    with allure.step("Go to users"):
        sidebar.open_users_page('Users', sidebar.users)
    with allure.step("Go to Devices"):
        sidebar.open_users_page('Devices', sidebar.devices)
    with allure.step("Go to Manufactured"):
        sidebar.open_users_page('Manufactured', sidebar.manufactured)
    with allure.step("Go to Calibration"):
        sidebar.open_users_page('Calibration', sidebar.calibration)
    with allure.step("Go to Video Markup"):
        sidebar.open_users_page('Video Markup', sidebar.video_markup)
