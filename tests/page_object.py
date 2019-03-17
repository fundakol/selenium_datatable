from items_list import Item, Container
from selenium.webdriver.common.by import By


class UserItem(Item):
    pass


class UserItems(Container):

    def __init__(self, how, what):
        super().__init__(how, what)
        locators_template = {
            'last_name': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(1)"),
            'first_name': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(2)"),
            'email': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(3)"),
            'due': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(4)"),
            'web_site': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(5)"),
            'delete_button': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#delete']"),
            'edit_button': (By.CSS_SELECTOR, "tr:nth-of-type({item_num}) td:nth-of-type(6) a[href='#edit']"),
        }
        self.item = UserItem(locators_template, self.current_item)

    @property
    def num_rows(self):
        return len(self.table.find_elements(By.CSS_SELECTOR, "tbody > tr"))

    @property
    def headers(self):
        elements = self.table.find_elements(By.CSS_SELECTOR, "thead > tr > th")
        return [element.text for element in elements]


class HomePage:
    items_list = UserItems(By.ID, "table1")

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)
        return self
