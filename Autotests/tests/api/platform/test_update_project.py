import json
from datetime import datetime

import allure
import pytest



@allure.id("21")
@allure.title("Update project")
@allure.label("component", "platform")
@allure.label("layer", "api")
@pytest.mark.skip(reason="Feature in progress.")
def test_update_project(platform_api_actions_researcher):
    with allure.step("Get project in DRAFT status with post get_projects/"):
        test_project = platform_api_actions_researcher.get_projects()

    with allure.step("Update full project info with put projects/{id}"):
        platform_api_actions_researcher.put_projects(project_id=test_project['id'],
                                                     title=f'AT_{str(datetime.now())}_patched',
                                                     interview_template={},
                                                     status='__READY_FOR_INTERVIEW__')
        assert platform_api_actions_researcher.get_project(project_id=test_project['id'])[
                   'status'] == '__READY_FOR_INTERVIEW__'

    with allure.step("Update status with patch projects/{id}"):
        upload_data = json.dumps({
            "status": "__ACTIVE__",
            })
        platform_api_actions_researcher.patch_projects(project_id=test_project['id'], data=upload_data)
        assert platform_api_actions_researcher.get_project(project_id=test_project['id'])['status'] == '__ACTIVE__'