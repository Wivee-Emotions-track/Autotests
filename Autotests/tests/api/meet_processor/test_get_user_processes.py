import allure



@allure.id("5")
@allure.title("Get user processes")
@allure.label("component", "meet_extension")
@allure.label("layer", "api")
def test_get_user_processes(meet_processor_api_actions):
    with allure.step("Get User Processes with /meet-processor/process/user-processes/"):
        processes = meet_processor_api_actions.get_user_processes()
        assert len(processes['items']) == 50
