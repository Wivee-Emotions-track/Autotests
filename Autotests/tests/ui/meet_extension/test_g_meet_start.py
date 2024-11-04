import allure
import pytest



@allure.id('2')
@allure.title("Meet extension login")
@allure.label("component", "meet_extension")
@allure.label("layer", "ui")
@pytest.mark.skip(reason="In progress.")
def test_meet_extension_login(google_meet_start_page):
    with allure.step("Google meet login"):
        google_meet_start_page.start_meet_instance()
        google_meet_start_page.screenshot('check.png')
