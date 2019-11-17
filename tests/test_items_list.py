import pytest

from selenium.webdriver import Chrome, ChromeOptions

from items_list import Item
from items_list.container import Container
from tests.page_object import HomePage


@pytest.fixture(scope='module')
def home_page(driver):
    return HomePage(driver, 'http://webserver:8000').open()


def test_get_headers(home_page):
    expected_headers = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']
    assert home_page.items_list.headers == expected_headers


def test_num_of_items(home_page):
    assert home_page.items_list.num_rows == 4


def test_get_item_by_row_id_1(home_page):
    item = home_page.items_list.get_item_by_position(1)

    assert item.first_name.text == 'John'
    assert item.last_name.text == 'Smith'
    assert item.email.text == 'jsmith@gmail.com'
    assert home_page.items_list.current_item == 1


def test_get_item_by_row_id_2(home_page):
    item = home_page.items_list.get_item_by_position(2)

    assert item.first_name.text == 'Frank'
    assert item.last_name.text == 'Bach'
    assert item.email.text == 'fbach@yahoo.com'
    assert 2 == home_page.items_list.current_item


def test_get_item_by_property_name(home_page):
    item = home_page.items_list.get_item_by_name('last_name', 'Doe')
    def test_get_item_by_row_id_3(self):
        item = self.page.items_list[2]

        self.assertEqual(item.first_name.text, 'Frank')
        self.assertEqual(item.last_name.text, 'Bach')
        self.assertEqual(item.email.text, 'fbach@yahoo.com')
        self.assertEqual(2, self.page.items_list.current_item)

    assert item.first_name.text == 'Jason'
    assert item.last_name.text == 'Doe'
    assert item.email.text == 'jdoe@hotmail.com'
    assert item.due.text == '$100.00'
    assert 3 == home_page.items_list.current_item
    def test_get_item_by_property_name_one_property(self):
        item = self.page.items_list.get_item_by_property(last_name='Doe')

        self.assertIsNotNone(item)
        self.assertEqual(item.first_name.text, 'Jason')
        self.assertEqual(item.last_name.text, 'Doe')
        self.assertEqual(item.email.text, 'jdoe@hotmail.com')
        self.assertEqual(item.due.text, '$100.00')
        self.assertEqual(3, self.page.items_list.current_item)


def test_locators(home_page):
    locators = home_page.items_list.item.locators
    assert 'last_name' in locators.keys()
    assert 'first_name' in locators.keys()
    current_item = home_page.items_list.current_item
    assert locators['last_name'] == ("css selector", "tr:nth-of-type({}) td:nth-of-type(1)".format(current_item))
    def test_get_item_by_property_name_two_properties(self):
        item = self.page.items_list.get_item_by_property(last_name='Doe', first_name='Jason')

        self.assertIsNotNone(item)
        self.assertEqual(item.first_name.text, 'Jason')
        self.assertEqual(item.last_name.text, 'Doe')
        self.assertEqual(item.email.text, 'jdoe@hotmail.com')
        self.assertEqual(item.due.text, '$100.00')
        self.assertEqual(3, self.page.items_list.current_item)

    def test_get_item_by_property_name_not_match(self):
        item = self.page.items_list.get_item_by_property(last_name='Doe', first_name='not match')
        self.assertIsNone(item)

    def test_locators(self):
        locators = self.page.items_list.item.locators
        self.assertIn('last_name', locators.keys())
        self.assertIn('first_name', locators.keys())
        current_item = self.page.items_list.current_item
        self.assertEqual(locators['last_name'], ("css selector", "tr:nth-of-type({}) td:nth-of-type(1)".format(current_item)))

    def test_implementation_exception(self):
        class RowItem(Item):
            locators_template = {'name': ('xpath', '//div')}

        class Table(Container):
            item = RowItem()

        table = Table('xpath', '//table')
        with self.assertRaises(NotImplementedError):
            table.get_headers_locator()
            table.get_row_locator()

    def test_implementation_exception(self):
        class RowItem(Item):
            locators_template = {'name': ('xpath', '//div')}

        class Table(Container):
            item = RowItem()

        table = Table('xpath', '//table')
        with self.assertRaises(NotImplementedError):
            table.get_headers_locator()
            table.get_row_locator()
