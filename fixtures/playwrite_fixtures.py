import os
import re

import allure
import pytest
from playwright.sync_api import sync_playwright

from configs.project_paths import SCREENSHOTS_PATH

DEFAULT_HEADLESS = True
DEFAULT_TIMEOUT = 5
BROWSERS = {
    "chromium": ["latest"]
    # "firefox": ["latest"],
    # "webkit": ["latest"]
    }


@pytest.fixture(scope='session', params=[(browser, version) for
                                         browser, versions in
                                         BROWSERS.items() for
                                         version in versions])
def browser_config(request):
    return request.param


@pytest.fixture(scope='session')
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope='function')
def browser(playwright, browser_config):
    browser_name, browser_version = browser_config
    browser_type = getattr(playwright, browser_name)

    if browser_version == 'latest':
        browser = browser_type.launch(headless=DEFAULT_HEADLESS, args=["--start-maximized"])

    else:
        executable_path = f'/path/to/{browser_name}-{browser_version}'
        browser = browser_type.launch(headless=DEFAULT_HEADLESS,
                                      executable_path=executable_path,
                                      args=["--window-size=1920,1080"])

    yield browser
    browser.close()


@pytest.fixture(scope='function')
def page(browser, request, fixture_additional_test_item_info):
    # context = browser.new_context(viewport={"width": 1920, "height": 900}, device_scale_factor=1)
    # context = browser.new_context()
    context = browser.new_context(no_viewport=True,
                                  viewport={"width": 1920, "height": 900},
                                  )

    page = context.new_page()
    page.evaluate("""
        document.documentElement.requestFullscreen();
    """)
    yield page

    screenshot_path = os.path.join(SCREENSHOTS_PATH, f'{request.config.args[0].replace("::", "_")}.png')
    clean_path = re.sub(r'[<>"|?*]', '_', screenshot_path)
    fixture_additional_test_item_info.screenshot_path = clean_path
    try:
        page.screenshot(path=clean_path)
        add_screenshot(clean_path)
    except TimeoutError:
        pass

    page.close()
    context.close()


def add_screenshot(screenshot_path):
    with open(screenshot_path, 'rb') as image:
        allure.attach(image.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
