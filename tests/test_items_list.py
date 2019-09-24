import unittest
from os import path
from selenium.webdriver import Chrome, ChromeOptions

from tests.page_object import HomePage

URL = path.join(path.abspath(path.join(path.dirname(__file__))), 'index.html')


class TestItemsList(unittest.TestCase):

    def setUp(self):
        options = ChromeOptions()
        options.headless = True
        self.driver = Chrome(options=options)
        self.page = HomePage(self.driver, URL)
        self.page.open()

    def test_get_headers(self):
        expected_headers = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']

        self.assertEqual(self.page.items_list.headers, expected_headers)

    def test_num_of_items(self):
        self.assertEqual(self.page.items_list.num_rows, 4)

    def test_get_item_by_row_id_1(self):
        item = self.page.items_list.get_item_by_position(1)

        self.assertEqual(item.first_name.text, 'John')
        self.assertEqual(item.last_name.text, 'Smith')
        self.assertEqual(item.email.text, 'jsmith@gmail.com')
        self.assertEqual(1, self.page.items_list.current_item)

    def test_get_item_by_row_id_2(self):
        item = self.page.items_list.get_item_by_position(2)

        self.assertEqual(item.first_name.text, 'Frank')
        self.assertEqual(item.last_name.text, 'Bach')
        self.assertEqual(item.email.text, 'fbach@yahoo.com')
        self.assertEqual(2, self.page.items_list.current_item)

    def test_get_item_by_property_name_one_property(self):
        item = self.page.items_list.get_item_by_property(last_name='Doe')

        self.assertIsNotNone(item)
        self.assertEqual(item.first_name.text, 'Jason')
        self.assertEqual(item.last_name.text, 'Doe')
        self.assertEqual(item.email.text, 'jdoe@hotmail.com')
        self.assertEqual(item.due.text, '$100.00')
        self.assertEqual(3, self.page.items_list.current_item)

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
        assert 'last_name' in locators.keys()
        assert 'first_name' in locators.keys()
        current_item = self.page.items_list.current_item
        assert locators['last_name'] == ("css selector", "tr:nth-of-type({}) td:nth-of-type(1)".format(current_item))

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
