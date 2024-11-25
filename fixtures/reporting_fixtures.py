import os
import re
import shutil

import allure
import pytest
from playwright._impl._errors import TargetClosedError

from configs.project_paths import LOGS_PATH, SCREENSHOTS_PATH, ALLURE_RESULTS_PATH, CHROME_COOKIES_PATH


@pytest.fixture(scope="session", autouse=True)
def clean_reporting_artifacts(worker_id):
    """Clear artifacts before running tests, only in the main thread"""
    if worker_id in ['gw0','master']:
        directories_to_clean = [
            SCREENSHOTS_PATH,
            ALLURE_RESULTS_PATH
        ]
        for directory in directories_to_clean:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)

        files_to_delete = [
            CHROME_COOKIES_PATH
            ]
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                os.remove(file_path)


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """Hook to take screenshot on test failure.
#     Execute all other hooks to obtain the report object & attach the screenshot to Allure report"""
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.failed:
#         page = item.funcargs.get('page')
#         if not page:
#             for key, value in item.funcargs.items():
#                 if '_page' in key:
#                     page = item.funcargs[key].page
#                     print(f"Available funcargs: {item.funcargs}")
#                     break
#
#         screenshot_path = os.path.join(SCREENSHOTS_PATH, f'{item.nodeid.replace("::", "_")}.png')
#         clean_path = re.sub(r'[<>:"/\\|?*]', '_', screenshot_path)
#         try:
#             page.screenshot(path=clean_path)
#             add_screenshot(clean_path)
#         except AttributeError:
#             pass


def add_screenshot(screenshot_path):
    with open(screenshot_path, 'rb') as image:
        allure.attach(image.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
