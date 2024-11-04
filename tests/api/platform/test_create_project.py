from datetime import datetime

import allure

from pytest_check import check

from helpers.allure_helper import set_allure_info


@allure.label("component", "platform")
@allure.label("layer", "api")
def test_create_project(allure_id, role, platform_api_actions, request):
    set_allure_info(allure_id=allure_id,
                    allure_title=f"Create project {role}")
    platform_api_actions = request.getfixturevalue(platform_api_actions)

    with allure.step("Create project with post projects/"):
        test_project = platform_api_actions.post_projects(
            title=f'AT_{str(datetime.now())}'
            )

    with allure.step("Get project info with get projects/{id}"):
        test_project = platform_api_actions.get_project(project_id=test_project['id'])

        check.equal(test_project['status'], "__DRAFT__",
                    f'Expected status: "__DRAFT__", actual: {test_project["status"]}')
