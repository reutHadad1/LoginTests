import re
import logging
from playwright.sync_api import Page, TimeoutError, Error

logging.basicConfig(filename='test_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        try:
            self.username_input = page.get_by_test_id("text-field-email-input").get_by_role("textbox")
            self.password_input = page.get_by_test_id("text-field-password-input").get_by_role("textbox")
            self.login_button = page.get_by_test_id("bo-dsm-common-button-contained-submit").get_by_test_id("bo-dsm-typography-button-root")
        except Error as e:
            logging.error(f"Error during initialization of locators: {str(e)}")
            raise

    def navigate(self):
        try:
            self.page.goto("https://web.eos.bnk-il.com/auth")
            self.page.wait_for_load_state('domcontentloaded')  
            logging.info("Page loaded successfully.")
        except TimeoutError:
            logging.error("Error: Page took too long to load.")
            raise
        except Error as e:
            logging.error(f"Unexpected error during navigation: {str(e)}")
            raise

    def login(self, username: str, password: str):
        if not self.validate_email(username):
            logging.error(f"Invalid email format: {username}")
            raise ValueError(f"Invalid email format: {username}")

        try:
            self.username_input.fill(username)
            self.password_input.fill(password)
            self.login_button.click()
            logging.info(f"Login attempted with username: {username}")
        except TimeoutError:
            logging.error("Error: Element interaction took too long.")
            raise
        except Error as e:
            logging.error(f"Unexpected error during login attempt: {str(e)}")
            raise

    def is_login_successful(self):
        try:
            # Check if the URL changed after login
            if self.page.url != "https://web.eos.bnk-il.com/auth":
                logging.info("Login successful.")
                return True
            logging.info("Login unsuccessful.")
            return False
        except Error as e:
            logging.error(f"Error during login success check: {str(e)}")
            raise

    def is_page_loaded(self):
        try:
            self.page.wait_for_load_state('domcontentloaded')

            # Wait explicitly for the username and password input to appear and be visible
            self.page.wait_for_selector('[data-testid="text-field-email-input"]', timeout=10000)
            self.page.wait_for_selector('[data-testid="text-field-password-input"]', timeout=10000)

            if not self.username_input.is_visible() or not self.password_input.is_visible():
                raise ValueError("Login page elements are not visible.")

            logging.info("Login page elements are visible and page is fully loaded.")
        except TimeoutError:
            logging.error("Error: Page elements took too long to load.")
            raise
        except Error as e:
            logging.error(f"Unexpected error during page load check: {str(e)}")
            raise
        except ValueError as ve:
            logging.error(f"Validation error: {str(ve)}")
            raise

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email using a regular expression."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None
