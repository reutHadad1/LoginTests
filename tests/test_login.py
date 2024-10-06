import pytest
import logging
from pages.login_page import LoginPage

logging.basicConfig(filename='test_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.mark.usefixtures("page")
class TestLogin:
    def test_login_functionality(self, page):
        login_page = LoginPage(page)

        try:
            logging.info("Navigating to the login page.")
            login_page.navigate()

            login_page.is_page_loaded()

            logging.info("Performing login with provided credentials.")
            login_page.login("john_doe@company.com", "123456")

            assert login_page.is_login_successful(), "Login was not successful"
            logging.info("Test passed: Login was successful.")

        except AssertionError as e:
            logging.error(f"Assertion error in test: {str(e)}")
            raise

        except Exception as e:
            logging.error(f"Unexpected error in test: {str(e)}")
            raise

