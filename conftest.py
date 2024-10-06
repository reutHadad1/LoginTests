import pytest
from playwright.sync_api import sync_playwright

# Adding a command-line option to specify the browser
def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chromium", help="Browser to run tests (chromium, firefox, webkit)"
    )

@pytest.fixture(scope="session")
def browser_type(pytestconfig):
    # Get the browser type from the command line option
    browser_name = pytestconfig.getoption("browser").lower()
    
    with sync_playwright() as p:
        if browser_name == "firefox":
            yield p.firefox
        elif browser_name == "webkit":
            yield p.webkit
        else:
            yield p.chromium

@pytest.fixture(scope="session")
def browser_instance(browser_type):
    # Initialize the browser instance for the session
    browser = browser_type.launch(headless=False)
    yield browser
    # Close the browser after all tests
    browser.close()

@pytest.fixture(scope="function")
def page(browser_instance):
    # Open a new page for each test and close it after the test
    page = browser_instance.new_page()
    yield page
    page.close()
