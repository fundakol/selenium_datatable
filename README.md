# selenium-datatable

[![PyPi](https://img.shields.io/pypi/v/selenium-datatable.png)](https://pypi.python.org/pypi/selenium-datatable)
[![Test](https://github.com/fundakol/selenium_datatable/actions/workflows/main.yml/badge.svg)](https://github.com/fundakol/selenium_datatable/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/fundakol/selenium_datatable/branch/master/graph/badge.svg)](https://codecov.io/gh/fundakol/selenium_datatable)

## Overview

A small library for simplifying a table object in selenium

## Installation
If you have pip on your system, you can simply install or upgrade the Python bindings:
```
pip install selenium-datatable
```
Alternately, you can download the source code and run:
```
python setup.py install
```

## Usage

A table object class implementation:
```python
# -- FILE: table.py
from selenium.webdriver.common.by import By
from selenium_datatable import DataTable, Column

class UsersTable(DataTable):
    rows_locator = (By.CSS_SELECTOR, "tbody > tr")
    headers_locator = (By.CSS_SELECTOR, "thead > tr > th")
    # columns
    last_name = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(1)")
    first_name = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(2)")
    email = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(3)")
    due = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(4)")
    web_site = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(5)")
    delete_button = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(6) a[href='#delete']")
    edit_button = Column(By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(6) a[href='#edit']")
```

A page object class implementation:
```python
# -- FILE: home_page.py
from table import UsersTable

class HomePage:    
    items_list = UsersTable("id", "table1")
   
    def __init__(self, driver, url='http://localhost/tables'):
        self.driver = driver
        self.url = url           
        
    def open(self):
        self.driver.get(self.url)
```

Unittest:
```python
# -- FILE: test_table.py
import unittest
from selenium.webdriver import Chrome
from home_page import HomePage

class TestTable(unittest.TestCase):

    def setUp(self):
        self.driver = Chrome()
        self.page = HomePage(self.driver)
        self.page.open()

    def test_get_item_from_first_row(self):        
        item = self.page.items_list.get_item_by_position(1)        
        self.assertEqual(item.first_name.text, 'John')
        self.assertEqual(item.last_name.text, 'Smith')
        self.assertEqual(item.email.text, 'jsmith@gmail.com')
    
    def test_get_item_by_property(self):
        item = self.page.items_list.get_item_by_property(last_name='Doe', first_name='Jason')    
        self.assertEqual(item.first_name.text, 'Jason')
        self.assertEqual(item.last_name.text, 'Doe')
    
    def test_number_of_rows(self):
        assert len(self.page.items_list) == 4
    
    def test_iterate_through_rows(self):
        for row in self.page.items_list:
            self.assertTrue(hasattr(row, 'last_name')) 
    
    def test_comprehension_list_slice(self):
        users = [row for row in self.page.items_list[1:3]]
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].first_name.text, "Frank")
        self.assertEqual(users[1].first_name.text, "Jason")

    def tearDown(self):
        self.driver.close()
```
The `DataTable` class is looking for a "driver" attribute in an owner class, but you can change that behaviour by overriding the attribute `driver_attribute` from the `DataTable` class. 

```python
class UsersTable(DataTable):
    ...
    driver_attribute = "selenium"
``` 
