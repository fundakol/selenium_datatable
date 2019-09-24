import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

PROJECT_DIR = os.path.dirname(os.path.join(os.path.abspath(__file__), '..'))


@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)
    driver.get('file:///{}/tests/index.html'.format(PROJECT_DIR))
    yield driver
    driver.close()
