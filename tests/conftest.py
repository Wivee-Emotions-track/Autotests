import os

import pytest
from dotenv import load_dotenv

from configs.project_paths import ROOT_DIR_PATH, ALLURE_RESULTS_PATH
from helpers.test_data_helper import load_test_data
from log import logger

pytest_plugins = [
    'fixtures.playwrite_fixtures',
    'fixtures.reporting_fixtures',

    'fixtures.extension_api_fixtures',
    'fixtures.extension_ui_fixtures',

    'fixtures.platform_api_fixtures',
    'fixtures.platform_ui_fixtures'
]

def pytest_configure(config):
    allure_dir = ALLURE_RESULTS_PATH
    config.option.allure_report_dir = allure_dir

def pytest_addoption(parser):
    """
        Adds a custom command-line options to pytest.
    """
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")

@pytest.fixture(scope="session", autouse=True)
def load_environment(request):
    """
        Fixture loads environment variables before running tests.
    """
    env_file = os.path.join(ROOT_DIR_PATH, '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        logger.error(f'Cannot find .env environment file: %s', env_file)

def pytest_generate_tests(metafunc):
    data = load_test_data(metafunc.definition)

    if data:
        keys = data[0].keys()

        processed_data = [
            {key: (value[0] if isinstance(value, list) and len(value) == 1 else value)
             for key, value in item.items()}
            for item in data
        ]

        metafunc.parametrize(
            ",".join(keys),
            [tuple(item[key] for key in keys) for item in processed_data]
        )