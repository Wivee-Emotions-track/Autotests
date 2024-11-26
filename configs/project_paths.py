import os

ROOT_DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(ROOT_DIR_PATH)

#reporting paths
LOGS_PATH = os.path.join(ROOT_DIR_PATH, 'reports', 'logs')
SCREENSHOTS_PATH = os.path.join(ROOT_DIR_PATH, 'reports', 'screenshots')
ALLURE_RESULTS_PATH = os.path.join(ROOT_DIR_PATH, 'reports', 'allure-results')

#resources
RESOURCES_PATH = os.path.join(ROOT_DIR_PATH, 'resources')
API_RESOURCES_PATH = os.path.join(RESOURCES_PATH, 'api')
UI_RESOURCES_PATH = os.path.join(RESOURCES_PATH, 'ui')
TEST_DATA_PATH = os.path.join(RESOURCES_PATH, 'test_data')

CHROME_COOKIES_PATH = os.path.join(UI_RESOURCES_PATH, 'chrome_cookies.json')

USERNAME = "dmitrijdmtirij@gmail.com"
PASSWORD = "Qwerty_0000"
