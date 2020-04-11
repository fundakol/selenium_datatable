import abc
import collections.abc
import copy
from typing import Union, Iterable, Optional, Tuple, List, Callable
from collections import namedtuple
import copy

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from .rowitem import RowItem

_error_msg = 'Attribute "{}" must be implemented as tuple("strategy", "locator")'


class Column:

    def __init__(self, how: str, what: str):
        self._how = how
        self._what = what

    @property
    def locator(self) -> Tuple[str, str]:
        return self._how, self._what

    def __repr__(self):
        return "{}(how='{}', what='{}')".format(self.__class__.__name__,
                                                self._how,
                                                self._what)

    def update_locator(self, row: int) -> None:
        self._what = self._what.format(row=row)


class Columns:

    def __init__(self, row: int, columns: dict, table: WebElement):
        self.row: int = row
        self.columns: dict = columns
        self._table: WebElement = table

    def __repr__(self):
        return 'Column(row="{}", columns={!r})'.format(self.row, self.columns.keys())

    def __getattr__(self, name):
        if name in self.columns:
            column_item = copy.copy(self.columns[name])
            column_item.update_locator(self.row)
            return self._table.find_element(*column_item.locator)
        raise AttributeError(name)


class TableMetaclass(type):

    def __new__(mcs, new, bases, attrs):
        _columns = dict()
        for key, value in attrs.items():
            if isinstance(value, Column):
                _columns[key] = value
        for key in _columns:
            attrs.pop(key)
        cls = super().__new__(mcs, new, bases, attrs)
        cls._columns = _columns
        return cls


class TableContainer(metaclass=TableMetaclass):
    rows_locator: Tuple[str, str] = None
    headers_locator: Tuple[str, str] = None
    driver_attrib: str = "driver"

    def __init__(self, how: str, what: str) -> None:
        self._table: Optional[WebElement] = None
        self._table_locator: Tuple[str, str] = (how, what)
        self.current_row: int = 0

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
        self._table = self._driver.find_element(*self._table_locator)
        return self

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        return Columns(index + 1, self._columns, self._table)

    def __next__(self):
        if self.current_row > len(self):
            self.current_row = 0
            raise StopIteration()
        item = self.__getitem__(self.current_row)
        self.current_row += 1
        return item

    def __len__(self):
        try:
            return len(self._table.find_elements(*self.get_rows_locator()))
        except NoSuchElementException:
            return 0

    @property
    def current_row(self) -> int:
        return self.__current_row + 1

    @current_row.setter
    def current_row(self, value: int) -> None:
        self.__current_row = value - 1

    # TODO: rename to get_row_by_position
    def get_item_by_position(self, row: int):
        return self.__getitem__(row)

    # TODO: rename to get_row_by_property
    def get_item_by_property(self, **kwargs) -> Union[RowItem, None]:
        for item in self.get_items_by_property(**kwargs):
            return item
        # raise AttributeError
        return None

    # TODO: rename to iter_rows_by_property
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
        elements = self._table.find_elements(*self.get_headers_locator())  # type: ignore
        return [element.text for element in elements]

    @property
    def columns(self) -> List[str]:
        """Return names of columns in the table"""
        return list(self._columns.items())

    def get_rows_locator(self) -> tuple:
        if self.rows_locator is None:
            raise NotImplementedError(_error_msg.format("rows_locator"))
        return self.rows_locator

    def get_headers_locator(self) -> tuple:
        if self.headers_locator is None:
            raise NotImplementedError(_error_msg.format("headers_locator"))
        return self.headers_locator
