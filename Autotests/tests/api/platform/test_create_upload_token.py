from time import sleep

import allure


from helpers.date_helper import expiry_date_difference


@allure.id("6")
@allure.title("Upload token")
@allure.label("component", "platform")
@allure.label("layer", "api")
def test_create_upload_token(platform_api_actions_researcher):
    old_access_token = platform_api_actions_researcher.token
    old_access_token_expiry = platform_api_actions_researcher.access_token_expiry

    with allure.step("Upload access token with /auth/token/refresh/"):
        sleep(2)
        platform_api_actions_researcher.update_access_token()

        assert old_access_token != platform_api_actions_researcher.token
        assert expiry_date_difference(old_access_token_expiry, platform_api_actions_researcher.access_token_expiry) >= 2
        platform_api_actions_researcher.update_access_token()
