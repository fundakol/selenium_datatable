import abc
import collections.abc
import copy
import warnings
from typing import Union, Iterable, Optional, Tuple, List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from .rowitem import RowItem

_error_msg = 'Attribute "{}" must be implemented as tuple("strategy", "locator")'

warnings.warn(f'Module {__name__} is deprecated.', DeprecationWarning)


class Container(abc.ABC, collections.abc.Sequence, collections.abc.Iterator):
    """Container class for Items list"""
    rows_locator: Optional[Tuple[str, str]] = None
    headers_locator: Optional[Tuple[str, str]] = None
    driver_attrib: str = "driver"

    def __init__(self, how: str, what: str) -> None:
        self.table: Optional[WebElement] = None
        self._table_locator: tuple = (how, what)
        self.current_row: int = 1

    @property
    @abc.abstractmethod
    def item(self) -> RowItem:
        """A single row item"""

    def __repr__(self):
        return '{}(how="{}", what="{}")'.format(self.__class__.__name__,
                                                self._table_locator[0],
                                                self._table_locator[1])

    def __get__(self, obj, owner):
        if not hasattr(obj, self.driver_attrib):
            exc_msg = 'Implementation error. Class "{}" has no attribute "{}"'
            raise AttributeError(exc_msg.format(obj.__class__.__name__,
                                                self.driver_attrib))
        self._driver = obj.driver
        self.table = self._driver.find_element(*self._table_locator)
        return self

    def __next__(self) -> RowItem:
        if self.current_row > len(self):
            self.current_row = 1
            raise StopIteration()
        item = self.get_item_by_position(self.current_row)
        self.current_row += 1
        return item

    def __len__(self):
        try:
            return len(self.table.find_elements(*self.get_rows_locator()))
        except NoSuchElementException:
            return 0

    def __getitem__(self, key: Union[int, slice]) -> RowItem:  # type: ignore
        return self.get_item_by_position(key + 1)  # type: ignore

    @property
    def current_row(self) -> int:
        return self.__current_row

    @current_row.setter
    def current_row(self, value: int) -> None:
        self.item.row_number = value
        self.__current_row = value

    def get_item_by_position(self, row: int) -> RowItem:
        """Get an item from row number (starting from 1)"""
        if row > self.num_rows:
            raise IndexError()
        self.current_row = row
        return copy.copy(self.item)

    def get_item_by_property(self, **kwargs) -> Union[RowItem, None]:
        for item in self.get_items_by_property(**kwargs):
            return item
        return None

    def get_items_by_property(self, **kwargs) -> Iterable[RowItem]:
        """An iterator"""
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
                yield item

    @property
    def num_rows(self) -> int:
        """Return a number of rows in the table"""
        return len(self)

    @property
    def headers(self) -> List[str]:
        """Return names of columns in the table"""
        elements = self.table.find_elements(*self.get_headers_locator())  # type: ignore
        return [element.text for element in elements]

    def get_rows_locator(self) -> tuple:
        if self.rows_locator is None:
            raise NotImplementedError(_error_msg.format("rows_locator"))
        return self.rows_locator

    def get_headers_locator(self) -> tuple:
        if self.headers_locator is None:
            raise NotImplementedError(_error_msg.format("headers_locator"))
        return self.headers_locator
