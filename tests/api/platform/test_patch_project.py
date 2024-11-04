import json

import allure
import pytest



@allure.id("3")
@allure.title("Patch project")
@allure.label("component", "platform")
@allure.label("layer", "api")
@pytest.mark.skip(reason="In progress.")
def test_patch_project(platform_api_actions_researcher):
    with allure.step("Get project in DRAFT status with post get_projects/"):
        test_project = platform_api_actions_researcher.get_projects()

    with allure.step("Update status with patch projects/{id}"):
        upload_data = json.dumps({
            "status": "__ACTIVE__",
            })
        platform_api_actions_researcher.patch_projects(project_id=test_project['id'], data=upload_data)
        assert platform_api_actions_researcher.get_project(project_id=test_project['id'])['status'] == '__ACTIVE__'
