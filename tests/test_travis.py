from tests.page_object import HomePage

URL = 'http://localhost:8000'


def test_get_headers(driver):
    page = HomePage(driver, URL)
    expected_headers = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']
    assert page.items_list.headers, expected_headers
