import allure

from helpers.check_helper import check_api_error


@allure.id("24")
@allure.title("Roles get brief")
@allure.label("component", "platform")
@allure.label("layer", "api")
@allure.label("story", "roles")
def test_get_brief_info(project_with_brief_customer, platform_api_actions_researcher):
    project = project_with_brief_customer[0]
    with allure.step("Researcher: get briefs in project. Invisible for researcher."):
        get_briefs_response = platform_api_actions_researcher.get_briefs(project['id'],
                                                                         check_response=False,
                                                                         convert_to_json=False)

        check_api_error(response=get_briefs_response,
                        expected_status_code=403,
                        expected_message='You do not have permission to perform this action.')
