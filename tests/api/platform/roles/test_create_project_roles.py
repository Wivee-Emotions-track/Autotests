from datetime import datetime

import allure

from pytest_check import check


@allure.id("12")
@allure.title("Roles create project customer")
@allure.label("component", "platform")
@allure.label("layer", "api")
@allure.label("story", "roles")
def test_create_project_customer(platform_api_actions_researcher, platform_api_actions_customer):
    with allure.step("Customer: create project with post projects/"):
        project = platform_api_actions_customer.post_projects(
            title=f'AT_{str(datetime.now())}'
            )
        project_id=project['id']
    with allure.step("Researcher: get created project. Must be visible for researcher."):
        try:
            platform_api_actions_researcher.get_project(project_id)
        except:
            check.fail(f'Project {project_id} must be visible for researcher.')


@allure.id("13")
@allure.title("Roles create project researcher")
@allure.label("component", "platform")
@allure.label("layer", "api")
@allure.label("story", "roles")
def test_create_project_researcher(platform_api_actions_researcher, platform_api_actions_customer):
    with allure.step("Researcher: create project with post projects/"):
        project = platform_api_actions_researcher.post_projects(
            title=f'AT_{str(datetime.now())}'
            )
        project_id=project['id']
    with allure.step("Customer: get created project. Project must be invisible."):
        try:
            platform_api_actions_customer.get_project(project_id, ok_codes={404})
        except:
            check.fail(f'Project {project_id} must be invisible for customer.')
