# Items List Pattern

Project was created to work with HTML table element


## Example of use

Items list implementation:
```python
# -- FILE: table.py
from items_list import Item, Container

class UserItem(Item):
    pass

class UserItems(Container):

    def __init__(self, how, what):
        super().__init__(how, what)
        locators_template = {
            'last_name': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(1)"),
            'first_name': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(2)"),
            'email': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(3)"),
            'due': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(4)"),
            'web_site': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(5)"),
            'delete_button': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#delete']"),
            'edit_button': ("css", "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#edit']"),
        }
        self.item = UserItem(locators_template, self.current_item)

    @property
    def num_rows(self):
        return len(self.table.find_elements("css", "tbody > tr"))
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

    def test_one(self):
        page = HomePage(self.driver)
        page.open()
        item = page.items_list.get_item_by_position(1)
        
        assert item.first_name.text == 'John'
        assert item.last_name.text == 'Smith'
        assert item.email.text == 'jsmith@gmail.com'

    def tearDown(self):
            self.driver.close()
```
