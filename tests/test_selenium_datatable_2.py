import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium_datatable import DataTable, Column


URL = 'http://webserver:8000'


class UsersTable(DataTable):
    rows_locator = (By.CSS_SELECTOR, "tbody > tr")
    headers_locator = (By.CSS_SELECTOR, "thead > tr > th")
    last_name = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(1)")
    first_name = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(2)")
    email = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(3)")
    due = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(4)")
    web_site = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(5)")
    delete_button = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(6) a[href='#delete']")
    edit_button = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(6) a[href='#edit']")


class HomePage:
    table1 = UsersTable(By.ID, "table1")
    empty_table = UsersTable(By.ID, "table2")
    table_does_not_exist = UsersTable(By.ID, "not_exist")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)
        return self


@pytest.fixture(scope='function')
def home_page(driver):
    return HomePage(driver, URL).open()


def test_get_headers(home_page):
    expected_headers = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']
    assert home_page.table1.headers == expected_headers


def test_num_of_rows(home_page):
    assert home_page.table1.num_rows == 4
    assert len(home_page.table1) == 4


def test_num_of_rows_in_empty_table(home_page):
    assert len(home_page.empty_table) == 0


def test_get_item_from_first_row(home_page):
    item = home_page.table1[0]

    assert item.first_name.text == 'John'
    assert item.last_name.text == 'Smith'
    assert item.email.text == 'jsmith@gmail.com'


def test_get_item_from_second_row(home_page):
    item = home_page.table1[1]

    assert item.first_name.text == 'Frank'
    assert item.last_name.text == 'Bach'
    assert item.email.text == 'fbach@yahoo.com'


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


def test_iter_table(home_page):
    users = [row for row in home_page.table1]
    assert len(users) == 4
    assert users[0].first_name.text == "John"
    assert users[1].first_name.text == "Frank"
    assert users[2].first_name.text == "Jason"
    assert users[3].first_name.text == "Tim"
