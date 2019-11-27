import pytest
from selenium.common.exceptions import NoSuchElementException

from selenium_datatable import Container, RowItem
from tests.page_object import HomePage, NoTablePage


URL = 'http://webserver:8000'


@pytest.fixture(scope='function')
def home_page(driver):
    return HomePage(driver, URL).open()


def test_get_headers(home_page):
    expected_headers = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']
    assert home_page.items_list.headers == expected_headers


def test_num_of_items(home_page):
    assert home_page.items_list.num_rows == 4
    assert len(home_page.items_list) == 4


def test_get_item_by_row_id_1(home_page):
    item = home_page.items_list.get_item_by_position(1)

    assert item.first_name.text == 'John'
    assert item.last_name.text == 'Smith'
    assert item.email.text == 'jsmith@gmail.com'
    assert home_page.items_list.current_row == 1


def test_get_item_by_row_id_2(home_page):
    item = home_page.items_list.get_item_by_position(2)

    assert item.first_name.text == 'Frank'
    assert item.last_name.text == 'Bach'
    assert item.email.text == 'fbach@yahoo.com'
    assert home_page.items_list.current_row == 2


def test_get_item_by_index_1(home_page):
    item = home_page.items_list[1]

    assert item.first_name.text == 'Frank'
    assert item.last_name.text == 'Bach'
    assert item.email.text == 'fbach@yahoo.com'
    assert home_page.items_list.current_row == 2


def test_get_last_item_by_index_2(home_page):
    item = home_page.items_list[3]

    assert (item.first_name.text, item.last_name.text) == ('Tim', 'Conway')
    assert item.first_name.text == 'Tim'
    assert item.last_name.text == 'Conway'
    assert item.email.text == 'tconway@earthlink.net'
    assert home_page.items_list.current_row == 4


def test_get_item_by_property_name_one_property(home_page):
    item = home_page.items_list.get_item_by_property(last_name='Doe')

    assert item is not None
    assert item.first_name.text == 'Jason'
    assert item.last_name.text == 'Doe'
    assert item.email.text == 'jdoe@hotmail.com'
    assert item.due.text == '$100.00'


def test_get_item_by_property_name_two_properties(home_page):
    item = home_page.items_list.get_item_by_property(last_name='Doe', first_name='Jason')

    assert item is not None
    assert item.first_name.text == 'Jason'
    assert item.last_name.text == 'Doe'
    assert item.email.text == 'jdoe@hotmail.com'
    assert item.due.text == '$100.00'


def test_get_item_by_property_name_not_match(home_page):
    item = home_page.items_list.get_item_by_property(last_name='Doe', first_name='not match')
    assert item is None


def test_locators(home_page):
    home_page.items_list.current_row = 1
    locators = home_page.items_list.item.locators
    assert 'last_name' in locators.keys()
    assert 'first_name' in locators.keys()
    assert locators['last_name'] == ("css selector", "tr:nth-of-type(1) td:nth-of-type(1)")


def test_implementation_exception_for_headers_locator():
    class User(RowItem):
        locators_template = {'name': ('xpath', '//div')}

    class Table(Container):
        item = User()

    table = Table('xpath', '//table')
    with pytest.raises(NotImplementedError):
        table.get_headers_locator()


def test_implementation_exception_for_rows_locator(driver):
    class User(RowItem):
        locators_template = {'name': ('xpath', '//div')}

    class Table(Container):
        item = User()

    class Page:
        table = Table('xpath', '//table')

        def __init__(self, driver_, url):
            self.driver = driver_
            self.url = url

    page = Page(driver, URL)
    with pytest.raises(NotImplementedError):
        page.table.get_rows_locator()


def test_no_such_element_exception(driver):
    page = NoTablePage(driver, URL)

    with pytest.raises(NoSuchElementException):
        page.items_list.get_item_by_position(100)


def test_attribute_error_exception(home_page):
    with pytest.raises(AttributeError):
        home_page.items_list.get_item_by_property(unknow="test")
