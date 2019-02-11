import unittest
from os import path
from selenium.webdriver import Chrome

from .page_object import HomePage

URL = path.join(path.abspath(path.join(path.dirname(__file__))), r'index.html')


class TestItemsList(unittest.TestCase):

    def setUp(self):
        self.driver = Chrome()
        self.page = HomePage(self.driver, URL)
        self.page.open()

    def test_get_headers(self):
        expected_headers = ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']

        self.assertEqual(self.page.items_list.headers, expected_headers)

    def test_num_of_items(self):
        self.assertEqual(self.page.items_list.num_rows, 4)

    def test_get_item_by_row_id(self):
        item = self.page.items_list.get_item_by_position(1)

        self.assertEqual(item.first_name.text, 'John')
        self.assertEqual(item.last_name.text, 'Smith')
        self.assertEqual(item.email.text, 'jsmith@gmail.com')

    def test_get_item_by_property_name(self):
        item = self.page.items_list.get_item_by_name('last_name', 'Doe')

        self.assertEqual(item.first_name.text, 'Jason')
        self.assertEqual(item.last_name.text, 'Doe')
        self.assertEqual(item.email.text, 'jdoe@hotmail.com')
        self.assertEqual(item.due.text, '$100.00')

    def tearDown(self):
            self.driver.close()
