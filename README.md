# selenium_datatable

[![Build Status](https://travis-ci.org/fundakol/selenium_datatable.svg?branch=master)](https://travis-ci.org/fundakol/selenium_datatable)
[![codecov](https://codecov.io/gh/fundakol/selenium_datatable/branch/master/graph/badge.svg)](https://codecov.io/gh/fundakol/selenium_datatable)

## Project description

A small library for simplifying a table object in selenium

## Installation

```
python setup.py install
```

## Example of use

Items list implementation:
```python
# -- FILE: table.py
from selenium_datatable import RowItem, Container

class UserItem(RowItem):
    locators_template = {
            'last_name': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(1)"),
            'first_name': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(2)"),
            'email': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(3)"),
            'due': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(4)"),
            'web_site': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(5)"),
            'delete_button': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#delete']"),
            'edit_button': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#edit']"),
        }

class UserItems(Container):
    item = UserItem()
    rows_locator = ("css selector", "tbody > tr")
    headers_locator = ("css selector", "tbody > tr")    
```

Example of page object class implementation:
```python
# -- FILE: home_page.py
from table import UserItems

class HomePage:    
    items_list = UserItems("id", "table1")
   
    def __init__(self, driver, url='http://localhost/tables'):
        self.driver = driver
        self.url = url           
        
    def open(self):
        self.driver.get(self.url)
```

Use in Unittest:
```python
# -- FILE: test_table.py
import unittest
from selenium.webdriver import Chrome
from home_page import HomePage

class TestTable(unittest.TestCase):

    def setUp(self):
        self.driver = Chrome()

    def test_get_item_from_first_row(self):
        page = HomePage(self.driver)
        page.open()
        item = page.items_list.get_item_by_position(1)
        
        self.assertEqual(item.first_name.text, 'John')
        self.assertEqual(item.last_name.text, 'Smith')
        self.assertEqual(item.email.text, 'jsmith@gmail.com')

    def tearDown(self):
            self.driver.close()
```
