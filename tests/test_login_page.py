from time import sleep
from config import config

import pytest
from playwright.sync_api import expect

from core.base_test import BaseTest
from core.logger import get_logger
from pages.login_page import LoginPage

@pytest.mark.order(1)
class TestLoginPage(BaseTest):

    def test_login_page_is_visible(self):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Calling navigate from login_page")
        LoginPage.navigate(self.page)
        expect(self.page).to_have_url(config.BASE_URL)

    def test_enter_valid_username_with_invalid_password(self):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Test enter valid username with invalid password")
        self.logger.info("Entering valid username")
        self.page.get_by_role("textbox", name="Username").fill(self.test_data["username"])
        self.logger.info("Entering invalid password")
        self.page.get_by_role("textbox", name="Password").fill("Admin12345")
        self.logger.info("Asserting invalid credentials alert message")
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_selector("[role='alert']")
        expect(self.page.get_by_role("alert").filter(has_text="Invalid credentials"))