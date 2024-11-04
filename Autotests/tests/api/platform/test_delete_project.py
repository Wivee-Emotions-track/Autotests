import allure
import pytest



@allure.id("1")
@allure.title("Delete project")
@allure.label("component", "platform")
@allure.label("layer", "api")
@pytest.mark.skip(reason="Unknown behavior.")
def test_delete_project(platform_api_actions_researcher):
    with allure.step("Get projects with get projects/"):
        projects = platform_api_actions_researcher.get_projects()
        project_id = projects['results'][-1]['id']
    with allure.step("Delete project with delete projects/{id}"):
        platform_api_actions_researcher.delete_project(project_id)
