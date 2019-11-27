import abc
from collections.abc import Iterator, Sequence
from typing import Union

from selenium.common.exceptions import NoSuchElementException

from .rowitem import RowItem


_error_msg = 'Attribute "{}" must be implemented as tuple("strategy", "locator")'


class Container(abc.ABC, Iterator, Sequence):
    """Container class for Items list"""
    rows_locator = None
    headers_locator = None

    @property
    @abc.abstractmethod
    def item(self) -> RowItem:
        """A single row item"""

    def __init__(self, how: str, what: str) -> None:
        self.__table_locator: tuple = (how, what)
        self.current_row: int = 1

    def __get__(self, obj, owner):
        self.__driver = obj.driver
        self.table = self.__driver.find_element(*self.__table_locator)
        return self

    def __iter__(self):
        self.current_row = 1
        return self

    def __next__(self) -> RowItem:
        if self.current_row > len(self):
            self.current_row = 1
            raise StopIteration
        item = self.get_item_by_position(self.current_row)
        self.current_row += 1
        return item

    def __len__(self):
        return len(self.table.find_elements(*self.get_rows_locator()))

    def __getitem__(self, item) -> RowItem:
        return self.get_item_by_position(item + 1)

    @property
    def current_row(self):
        return self.__current_row

    @current_row.setter
    def current_row(self, value):
        self.item.update_locators(value)
        self.__current_row = value

    def get_item_by_position(self, row_number: int):
        """Get item from row number (starting from 1)"""
        self.current_row = row_number
        self.item.item_number = self.current_row
        for item_name, locator in self.item.locators.items():
            try:
                element = self.table.find_element(*locator)
            except NoSuchElementException:
                element = None
            setattr(self.item, item_name, element)
        return self.item

    def get_item_by_property(self, **kwargs) -> Union[RowItem, None]:
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
    def headers(self) -> list:
        elements = self.table.find_elements(*self.get_headers_locator())
        return [element.text for element in elements]

    def get_rows_locator(self) -> tuple:
        if self.rows_locator is None:
            raise NotImplementedError(_error_msg.format("row_locator"))
        return self.rows_locator

    def get_headers_locator(self) -> tuple:
        if self.headers_locator is None:
            raise NotImplementedError(_error_msg.format("headers_locator"))
        return self.headers_locator
