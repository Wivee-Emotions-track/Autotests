import pytest
from playwright.sync_api import sync_playwright

DEFAULT_HEADLESS = False
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


@pytest.fixture(scope='session')
def browser(playwright, browser_config):
    browser_name, browser_version = browser_config
    browser_type = getattr(playwright, browser_name)

    if browser_version == 'latest':
        browser = browser_type.launch(headless=DEFAULT_HEADLESS, args=["--start-fullscreen"])

    else:
        executable_path = f'/path/to/{browser_name}-{browser_version}'
        browser = browser_type.launch(headless=DEFAULT_HEADLESS,
                                      executable_path=executable_path,
                                      args=["--window-size=1920,1080"])

    yield browser
    browser.close()


@pytest.fixture(scope='function')
def page(browser):
    context = browser.new_context(viewport={"width": 1920, "height": 900},device_scale_factor=1)
    # context = browser.new_context()

    page = context.new_page()
    page.evaluate("""
        document.documentElement.requestFullscreen();
    """)
    yield page
    # page.close()
    context.close()
