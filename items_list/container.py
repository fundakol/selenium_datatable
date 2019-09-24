import abc

from selenium.common.exceptions import NoSuchElementException

from .item import Item


class Container(metaclass=abc.ABCMeta):
    """Container class for Items list"""

    @property
    @abc.abstractmethod
    def item(self) -> Item:
        pass

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
    @abc.abstractmethod
    def num_rows(self) -> int:
        """Return a number of rows in the table"""

    @property
    def current_item(self) -> int:
        """Return the current row"""
        return self.__current_item

    @property
    def headers(self):
        raise NotImplementedError()
