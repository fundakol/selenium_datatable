import pytest
from selenium.common.exceptions import NoSuchElementException

from selenium_datatable import Container, RowItem
from tests.page_object import HomePage, NoDriverPage


@pytest.fixture(scope='function')
def home_page(driver, url):
    return HomePage(driver, url).open()


def test_get_headers(home_page):
    expected_headers = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']
    assert home_page.table1.headers == expected_headers


def test_num_of_items(home_page):
    assert home_page.table1.num_rows == 4
    assert len(home_page.table1) == 4


def test_num_of_items_in_empty_table(home_page):
    assert len(home_page.empty_table) == 0


def test_get_item_by_row_id_1(home_page):
    item = home_page.table1.get_item_by_position(1)

    assert item.first_name.text == 'John'
    assert item.last_name.text == 'Smith'
    assert item.email.text == 'jsmith@gmail.com'
    assert home_page.table1.current_row == 1


def test_get_item_by_row_id_2(home_page):
    item = home_page.table1.get_item_by_position(2)

    assert item.first_name.text == 'Frank'
    assert item.last_name.text == 'Bach'
    assert item.email.text == 'fbach@yahoo.com'
    assert home_page.table1.current_row == 2


def test_get_item_by_index_1(home_page):
    item = home_page.table1[1]

    assert item.first_name.text == 'Frank'
    assert item.last_name.text == 'Bach'
    assert item.email.text == 'fbach@yahoo.com'
    assert home_page.table1.current_row == 2


def test_get_last_item_by_index_2(home_page):
    item = home_page.table1[3]

    assert (item.first_name.text, item.last_name.text) == ('Tim', 'Conway')
    assert item.first_name.text == 'Tim'
    assert item.last_name.text == 'Conway'
    assert item.email.text == 'tconway@earthlink.net'
    assert home_page.table1.current_row == 4


def test_get_item_by_property_name_one_property(home_page):
    item = home_page.table1.get_item_by_property(last_name='Doe')

    assert item is not None
    assert item.first_name.text == 'Jason'
    assert item.last_name.text == 'Doe'
    assert item.email.text == 'jdoe@hotmail.com'
    assert item.due.text == '$100.00'


def test_get_item_by_property_name_two_properties(home_page):
    item = home_page.table1.get_item_by_property(last_name='Doe', first_name='Jason')

    assert item is not None
    assert item.first_name.text == 'Jason'
    assert item.last_name.text == 'Doe'
    assert item.email.text == 'jdoe@hotmail.com'
    assert item.due.text == '$100.00'


def test_get_item_by_property_name_not_match(home_page):
    item = home_page.table1.get_item_by_property(last_name='Doe', first_name='not match')
    assert item is None


def test_locators(home_page):
    home_page.table1.current_row = 1
    locators = home_page.table1.item.locators
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


def test_implementation_exception_for_rows_locator(driver, url):
    class User(RowItem):
        locators_template = {'name': ('xpath', '//div')}

    class Table(Container):
        item = User()

    class Page:
        table = Table('xpath', '//table')

        def __init__(self, driver_, url):
            self.driver = driver_
            self.url = url

    page = Page(driver, url)
    with pytest.raises(NotImplementedError):
        page.table.get_rows_locator()


def test_no_such_element_exception(driver, home_page):
    with pytest.raises(NoSuchElementException):
        home_page.table_does_not_exist.get_item_by_position(100)


def test_attribute_error_exception(home_page):
    with pytest.raises(AttributeError):
        home_page.table1.get_item_by_property(unknow="test")


def test_sequence(home_page):
    names = "John Frank Jason Tim".split(' ')
    for row in home_page.table1:
        names.remove(row.first_name.text)
    assert names == []


def test_comprehension_list(home_page):
    users = [row for row in home_page.table1]
    assert len(users) == 4
    assert users[0].first_name.text == "John"
    assert users[1].first_name.text == "Frank"
    assert users[2].first_name.text == "Jason"
    assert users[3].first_name.text == "Tim"


def test_raise_exception_when_no_driver_attribute():
    page = NoDriverPage()
    with pytest.raises(AttributeError):
        page.users_table.get_item_by_position(1)
