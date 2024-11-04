from datetime import datetime

import allure

from pytest_check import check

from helpers.check_helper import check_api_error


@allure.id('10')
@allure.title('Customer brief flow')
@allure.label('component', 'platform')
@allure.label('layer', 'api')
def test_customer_brief_flow(platform_api_actions_customer):
    with allure.step('Create project with post /api/projects/'):
        project = platform_api_actions_customer.post_projects(title=f'AT_{str(datetime.now())}')

    with allure.step('Check that no brief in new project with get /api/brief-form/{id}/'):
        get_briefs_response = platform_api_actions_customer.get_briefs(project['id'])
        check.equal(get_briefs_response, '', f'Expected: no brief in new project, Actual: {get_briefs_response}')

    with allure.step('Create empty brief with post /api/brief-form/{id}/'):
        brief = platform_api_actions_customer.post_brief(project['id'])
        check.equal(brief['status'], '__DRAFT__',
                    f'Expected brief status: __DRAFT__ Actual brief status: {brief["status"]}')

    with allure.step('Try post /api/brief-form/{id}/ again. Already exists.'):
        post_brief_response = platform_api_actions_customer.post_brief(project['id'],
                                                                       check_response=False,
                                                                       convert_to_json=False)
        check_api_error(response=post_brief_response,
                        expected_status_code=400,
                        expected_message='Client brief with this Project already exists.')

    with allure.step('Patch brief with patch /api/brief-form/{id}/'):
        brief = platform_api_actions_customer.patch_brief(brief['id'])

    with allure.step('Send brief with patch /api/brief-form/{id}/save-and-send/'):
        keys_to_remove = {'id', 'project', 'status'}
        brief_data = {k: v for k, v in brief.items() if k not in keys_to_remove}
        brief = platform_api_actions_customer.patch_save_and_send(brief_id=brief['id'], test_data=brief_data)

        check.equal(brief['status'], '__SENT__',
                    f'Expected brief status: __SENT__ Actual brief status: {brief["status"]}')

        project_status = platform_api_actions_customer.get_project(project['id'])['status']
        check.equal(project_status, '__WAIT_FOR_PAYMENT__',
                    f'Expected project status: __WAIT_FOR_PAYMENT__ Actual project status: {project_status}')

    with allure.step('Try patch /api/brief-form/{id}/save-and-send/ again. Impossible.'):
        patch_save_and_send_response = platform_api_actions_customer.patch_save_and_send(brief_id=brief['id'],
                                                                                         test_data=brief_data,
                                                                                         check_response=False,
                                                                                         convert_to_json=False)
        check_api_error(response=patch_save_and_send_response,
                        expected_status_code=403)

    with allure.step('Try patch /api/brief-form/{id}/ again. Impossible.'):
        patch_brief_response = platform_api_actions_customer.patch_brief(brief['id'],
                                                                         check_response=False,
                                                                         convert_to_json=False)
        check_api_error(response=patch_brief_response,
                        expected_status_code=403)
