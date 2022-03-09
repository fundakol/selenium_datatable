import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .mock_http_server import MockServer


@pytest.fixture(scope='session')
def url():
    return 'http://localhost:5002'


@pytest.fixture(scope='session')
def driver(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    yield driver
    driver.close()


@pytest.fixture(scope='session', autouse=True)
def http_server():
    server = MockServer(5002)
    server.start()
    yield
    server.shutdown_server()
