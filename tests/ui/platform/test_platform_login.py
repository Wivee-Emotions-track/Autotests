import os

import allure
import pytest



@allure.id('8')
@allure.title("Platform success login")
@allure.label("component", "platform")
@allure.label("layer", "ui")
def test_successful_login(platform_login_page):
    with allure.step("Authorize with valid credentials"):
        platform_login_page.login(username=os.getenv('GOOGLE_LOGIN'),
                                  password=os.getenv('GOOGLE_PASSWORD'))


@allure.id('9')
@allure.title("Platform login - incorrect login")
@allure.label("component", "platform")
@allure.label("layer", "ui")
@pytest.mark.skip(reason="Feature in progress.")
def test_incorrect_password_login(platform_login_page):
    with allure.step("Enter login  @"):
        pass
    with allure.step("Enter login without ."):
        pass
    with allure.step("Authorize with incorrect password."):
        platform_login_page.login(username=os.getenv('GOOGLE_LOGIN'),
                                  password='wrong_password')
        platform_login_page.check_alert_message('Invalid username or password')
        platform_login_page.reload()
    with allure.step("Authorize with incorrect login."):
        platform_login_page.login(username='incorrect_email@df.er',
                                  password=os.getenv('GOOGLE_PASSWORD'))
        platform_login_page.check_alert_message('Invalid username or password')
