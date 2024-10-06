#Login Automation Project

This project automates the login functionality of a web application using Playwright. The tests are written in Python and utilize the pytest framework for easy execution and management.

#Features

Browser Compatibility: Supports multiple browsers (Chromium, Firefox, WebKit).
Login Functionality Testing: Automates the login process and validates whether the login was successful.
Error Handling: Captures and logs errors for better debugging.
Command-Line Options: Allows users to specify which browser to use when running tests.

#Prerequisites

Before running the tests, ensure you have the following installed:

Python 3.x
pip (Python package manager)

#Installation

Clone the repository:
git clone https://github.com/reutHadad1/LoginTests.git
cd LoginTests

playwright install


#Running Tests

pytest --browser=chromium
Replace chromium with firefox or webkit to test on those browsers
