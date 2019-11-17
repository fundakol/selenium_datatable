import abc
from collections.abc import Iterator, Sequence

from selenium.common.exceptions import NoSuchElementException

from .item import Item


error_msg = 'Attribute "{}" must be implemented as tuple("strategy", "locator")'


class Container(abc.ABC, Iterator, Sequence):
    """Container class for Items list"""
    row_locator = None
    headers_locator = None

    @property
    @abc.abstractmethod
    def item(self) -> Item:
        """A single row item"""

    def __init__(self, how: str, what: str) -> None:
        self.__table_locator: tuple = (how, what)
        self.__current_item: int = 1

    def __get__(self, obj, owner):
        self.__driver = obj.driver
        self.table = self.__driver.find_element(*self.__table_locator)
        return self

    def __iter__(self):
        self.__item_index = 1
        return self

    def __next__(self):
        if self.__item_index > len(self):
            self.__item_index = 1
            raise StopIteration
        item = self.get_item_by_position(self.__item_index)
        self.__item_index += 1
        return item

    def __len__(self):
        return len(self.table.find_elements(*self.get_row_locator()))

    def __getitem__(self, item) -> Item:
        return self.get_item_by_position(item)

    def get_item_by_position(self, row_number: int):
        self.__current_item = row_number
        self.item.item_number = self.__current_item
        for item_name, locator in self.item.locators.items():
            try:
                element = self.table.find_element(*locator)
            except NoSuchElementException:
                element = None
            setattr(self.item, item_name, element)
        return self.item

    def get_item_by_property(self, **kwargs):
        for item in self:
            match = False
            for key, value in kwargs.items():
                property_ = getattr(item, key, None)
                if property_ is None:
                    raise AttributeError(key)
                if property_.text == value:
                    match = True
                else:
                    match = False
                    break
            if match:
                return item
        return None

    @property
    def num_rows(self) -> int:
        """Return a number of rows in the table"""
        return self.__len__()

    @property
    def current_item(self) -> int:
        """Return the current row"""
        return self.__current_item

    @property
    def headers(self) -> list:
        elements = self.table.find_elements(*self.get_headers_locator())
        return [element.text for element in elements]

    def get_row_locator(self) -> tuple:
        if self.row_locator is None:
            raise NotImplementedError(error_msg.format("row_locator"))
        return self.row_locator

    def get_headers_locator(self) -> tuple:
        if self.headers_locator is None:
            raise NotImplementedError(error_msg.format("headers_locator"))
        return self.headers_locator
