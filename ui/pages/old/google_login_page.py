import os
import uuid

import allure
from playwright.sync_api import Page

from configs.project_paths import SCREENSHOTS_PATH
from decorators.waits import retry_on_exception, measure_execution_time
from helpers.anty_capcha import AntiGateClient
from log import logger
from ui.locators.old.google_account_page_locators import GoogleAccountPageLocators
from ui.locators.old.google_login_page_locators import GoogleLoginPageLocators
from ui.pages.base_page import BasePage
from playwright._impl._errors import TimeoutError


class GoogleLoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page,
                         url='https://accounts.google.com/ServiceLogin')
        self.capcha_screenshot_path = None

    def login(self, username, password):
        try:
            self.type_in(locator=GoogleLoginPageLocators.EMAIL_INPUT,
                         data=username)
            self.type_in(locator=GoogleLoginPageLocators.PASSWORD_INPUT,
                         data=password)
            self.wait_for_selector(locator=GoogleAccountPageLocators.GOOGLE_ACCOUNT_HEADER)
        except TimeoutError:
            self.login_with_capcha(username, password)
            self.screenshot(file_name='after_capcha_login_success_page.png')

    @measure_execution_time
    @retry_on_exception(steps=30)
    def login_with_capcha(self, username, password):
        self.type_in(locator=GoogleLoginPageLocators.EMAIL_INPUT,
                     data=username)
        self.wait_for_selector(GoogleLoginPageLocators.CAPCHA_IMG)

        capcha_id, capcha_screenshot_path = self.make_capcha_screen()

        antigate = AntiGateClient()
        logger.info('Antigate balance: %s $', antigate.balance())
        logger.debug('Antigate start process for capcha  %s', self.capcha_screenshot_path)
        try:
            capcha_value = antigate.captcha_handler(capcha_screenshot_path)
            self.type_in(locator=GoogleLoginPageLocators.CAPCHA_INPUT,
                         data=capcha_value)
            self.type_in(locator=GoogleLoginPageLocators.PASSWORD_INPUT,
                         data=password)
            self.wait_for_selector(locator=GoogleAccountPageLocators.GOOGLE_ACCOUNT_HEADER)
        except TimeoutError:
            antigate.abuse()
            self.page.reload()

    def make_capcha_screen(self):
        capcha_img_src = self.page.get_attribute(GoogleLoginPageLocators.CAPCHA_IMG, 'src')

        capcha_img_url = 'https://accounts.google.com' + capcha_img_src
        capcha_img_page = self.page.context.new_page()
        capcha_img_page.goto(capcha_img_url)

        capcha_id = str(uuid.uuid4())
        capcha_screenshot_path = os.path.join(SCREENSHOTS_PATH, f'ca_{capcha_id}.jpg')
        capcha_img_page.screenshot(path=capcha_screenshot_path)
        allure.attach.file(capcha_screenshot_path, name=f'ca_{capcha_id}.jpg',
                           attachment_type=allure.attachment_type.JPG)
        capcha_img_page.close()
        return capcha_id, capcha_screenshot_path
