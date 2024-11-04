import allure


def set_allure_info(allure_id: str, allure_title: str, description=None):
    allure.dynamic.id(allure_id)
    allure.dynamic.title(allure_title)
    if description:
        allure.dynamic.description(description)