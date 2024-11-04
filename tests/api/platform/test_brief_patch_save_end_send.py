import allure

from pytest_check import check

from helpers.allure_helper import set_allure_info
from helpers.dict_helper import compare_dicts


@allure.label("component", "platform")
@allure.label("layer", "api")
def test_brief_patch_save_end_send(allure_id, allure_title, description,
                                   brief_data, expected_response, ok_code,
                                   project_with_brief_customer, platform_api_actions_customer):
    set_allure_info(allure_id=allure_id,
                    allure_title=allure_title,
                    description=description)

    brief = project_with_brief_customer[1]

    with allure.step('Send brief with patch /api/brief-form/{id}/save-and-send/'):
        actual_response = platform_api_actions_customer.patch_save_and_send(brief_id=brief['id'], test_data=brief_data, ok_codes={ok_code})
        if not expected_response:
            expected_response = platform_api_actions_customer.get_brief(brief_id=brief['id'])

        diff = compare_dicts(expected_response, actual_response,
                             exclude_paths={"root['id']", "root['project']", "root['status']"})

        err_mess_str = '\n'.join(diff[1])
        check.is_false(diff[0], msg=err_mess_str)
