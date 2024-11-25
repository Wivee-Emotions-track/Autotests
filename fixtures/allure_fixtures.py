from dataclasses import dataclass

import pytest


@dataclass
class TestItemAdditionalInfo:
    """Class for additional test data"""

    video_link: str = None
    user_data = None
    screenshot_path: str = None
    path_to_logs: str = None
    allure_report: str = None


@pytest.fixture(scope="function", autouse=True)
def fixture_additional_test_item_info():
    return TestItemAdditionalInfo()
