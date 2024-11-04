from playwright.sync_api import Page

from decorators.waits import retry_on_exception
from ui.locators.google_meet_base_page_locators import GoogleMeetBasePageLocators
from ui.pages.base_page import BasePage


class GoogleMeetBasePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page, url='https://meet.google.com/')

    @retry_on_exception()
    def start_meet_instance(self):
        """
            Starts a new Google Meet instance by:
            - Clicking the 'New Meeting' button.
            - Clicking the 'Start an Instant Meeting' with a reduced timeout of 5000 milliseconds (5 seconds)
            to speed up the process in case of unstable click.
        """
        self.click(GoogleMeetBasePageLocators.NEW_MEETING_BUTTON)
        self.click(GoogleMeetBasePageLocators.START_AN_INSTANT_MEETING_BUTTON,
                   timeout=5000)
