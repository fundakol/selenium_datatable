from items_list import Item, Container
from selenium.webdriver.common.by import By


class UserItem(Item):
    locators_template = {
        'last_name': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(1)"),
        'first_name': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(2)"),
        'email': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(3)"),
        'due': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(4)"),
        'web_site': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(5)"),
        'delete_button': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#delete']"),
        'edit_button': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#edit']"),
    }


class UserItems(Container):
    row_locator = (By.CSS_SELECTOR, "tbody > tr")
    headers_locator = (By.CSS_SELECTOR, "thead > tr > th")
    item = UserItem()


class HomePage:
    items_list = UserItems(By.ID, "table1")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)
        return self
