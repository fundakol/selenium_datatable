from typing import Union, Iterable, Optional, Tuple, List
import copy

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

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
        return '{}(row="{}", columns={!r})'.format(self.__class__.__name__,
                                                   self.row, self.columns.keys())

    def __getattr__(self, name):
        if name in self.columns:
            column_item = copy.copy(self.columns[name])
            column_item.update_locator(self.row)
            try:
                return self._table.find_element(*column_item.locator)
            except NoSuchElementException:
                return None
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


class DataTable(metaclass=TableMetaclass):
    rows_locator: Tuple[str, str] = None
    headers_locator: Tuple[str, str] = None
    driver_attrib: str = "driver"

    def __init__(self, how: str, what: str) -> None:
        self._table: Optional[WebElement] = None
        self._table_locator: Tuple[str, str] = (how, what)
        self.current_row: int = 1

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
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return [Columns(i + 1, self._columns, self._table)
                    for i in range(start, stop, step)]
        elif isinstance(index, int):
            if 0 <= index < len(self):
                return Columns(index + 1, self._columns, self._table)
            else:
                raise IndexError
        else:
            raise TypeError('Invalid argument type: {}'.format(type(index)))

    def __next__(self):
        if self.current_row > len(self):
            self.__current_row = 0
            raise StopIteration()
        item = self.__getitem__(self.__current_row)
        self.__current_row += 1
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
        if value < 1:
            raise ValueError('current_row cannot be less then 1')
        self.__current_row = value - 1

    def get_item_by_position(self, row: int):
        """Return item from the row."""
        self.current_row = row
        return self.__getitem__(self.__current_row)

    def get_item_by_property(self, **kwargs) -> Union[Columns, None]:
        """Return first row matching given properties"""
        for item in self.get_items_by_property(**kwargs):
            return item
        return None

    def get_items_by_property(self, **kwargs) -> Iterable[Columns]:
        """Iterate over rows and return every row matching given properties"""
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
        """Return names of columns in header row in the table"""
        elements = self._table.find_elements(*self.get_headers_locator())  # type: ignore
        return [element.text for element in elements]

    @property
    def columns(self) -> List[str]:
        """Return names of defined columns"""
        return list(self._columns.items())

    def get_rows_locator(self) -> tuple:
        if self.rows_locator is None:
            raise NotImplementedError(_error_msg.format("rows_locator"))
        return self.rows_locator

    def get_headers_locator(self) -> tuple:
        if self.headers_locator is None:
            raise NotImplementedError(_error_msg.format("headers_locator"))
        return self.headers_locator
