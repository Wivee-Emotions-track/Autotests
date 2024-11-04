import os
from datetime import datetime

import allure
import pytest

from api.platform.platform_actions import PlatformApiActions
from log import logger


@pytest.fixture(scope="function")
def platform_api_actions_researcher():
    logger.debug(f"platform login as researcher {os.getenv('PLATFORM_RESEARCHER_LOGIN')}...")
    platform_api_actions = PlatformApiActions(endpoint=os.getenv('PLATFORM_URL'),
                                              user_email=os.getenv('PLATFORM_RESEARCHER_LOGIN'),
                                              user_password=os.getenv('PLATFORM_RESEARCHER_PASSWORD'))
    logger.debug(f"Success!")

    return platform_api_actions


@pytest.fixture(scope="function")
def platform_api_actions_customer():
    logger.debug(f"platform login as customer {os.getenv('PLATFORM_CUSTOMER_LOGIN')}...")
    platform_api_actions = PlatformApiActions(endpoint=os.getenv('PLATFORM_URL'),
                                                      user_email=os.getenv('PLATFORM_CUSTOMER_LOGIN'),
                                                      user_password=os.getenv('PLATFORM_CUSTOMER_PASSWORD'))
    logger.debug(f"Success!")
    return platform_api_actions

@pytest.fixture(scope="function")
def project_with_brief_customer(platform_api_actions_customer):
    with allure.step('Precondition step: Customer creates project with brief.'):
        project = platform_api_actions_customer.post_projects(title=f'AT_{str(datetime.now())}')
        brief = platform_api_actions_customer.post_brief(project['id'])
        brief = platform_api_actions_customer.patch_brief(brief['id'])
    return project, brief