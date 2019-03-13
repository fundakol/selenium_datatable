import abc

from selenium.common.exceptions import NoSuchElementException


class Container(metaclass=abc.ABCMeta):
    """Container class for Items list"""

    def __init__(self, how: str, what: str):
        self.item = None
        self.__driver = None
        self.__table_locator = (how, what)
        self.__current_item = 1

    def __get__(self, obj, owner):
        self.__driver = obj.driver
        self.table = self.__driver.find_element(*self.__table_locator)
        return self

    def __iter__(self):
        self.__item_index = 1
        return self

    def __next__(self):
        if self.__item_index > self.num_rows:
            self.__item_index = 1
            raise StopIteration
        item = self.get_item_by_position(self.__item_index)
        self.__item_index += 1
        return item

    def get_item_by_position(self, row_number: int):
        self.__current_item = row_number
        self.item.update_item_number(self.__current_item)
        for item_name, locator in self.item.locators.items():
            try:
                element = self.table.find_element(*locator)
            except NoSuchElementException:
                element = None
            setattr(self.item, item_name, element)
        return self.item

    def get_item_by_name(self, property_name: str, value: str):
        for item in self:
            property = getattr(item, property_name, None)
            assert property is not None
            if property.text == value:
                return item
        return None

    @property
    @abc.abstractmethod
    def num_rows(self):
        pass

    @property
    def current_item(self):
        return self.__current_item

    @property
    def headers(self):
        raise NotImplemented