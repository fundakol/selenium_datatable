# selenium-datatable

[![Build Status](https://travis-ci.org/fundakol/selenium_datatable.svg?branch=master)](https://travis-ci.org/fundakol/selenium_datatable)
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
from selenium_datatable import RowItem, Container

class UserItem(RowItem):
    locators_template = {
        'last_name': ("css", "tr:nth-of-type({row}) td:nth-of-type(1)"),
        'first_name': ("css", "tr:nth-of-type({row}) td:nth-of-type(2)"),
        'email': ("css", "tr:nth-of-type({row}) td:nth-of-type(3)"),
        'due': ("css", "tr:nth-of-type({row}) td:nth-of-type(4)"),
        'web_site': ("css", "tr:nth-of-type({row}) td:nth-of-type(5)"),
        'delete_button': ("css", "tr:nth-of-type({row}) td:nth-of-type(6) a[href='#delete']"),
        'edit_button': ("css", "tr:nth-of-type({row}) td:nth-of-type(6) a[href='#edit']"),
        }

class UserItems(Container):
    item = UserItem()
    rows_locator = ("css selector", "tbody > tr")
    headers_locator = ("css selector", "tbody > tr")    
```

A page object class implementation:
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

Unittest:
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
The Container class is looking for a "driver" attribute in an owner class, but you can change that behaviour by overiding the attribute _driver_attribute_ from the Container class. 

```python
class UserItems(Container):
    item = UserItem()
    rows_locator = ("css selector", "tbody > tr")
    headers_locator = ("css selector", "tbody > tr")    
    driver_attribute = "selenium"
```  
