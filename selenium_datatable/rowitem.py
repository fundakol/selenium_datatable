import abc
import warnings
from typing import Dict

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

warnings.warn('Module is deprecated.', DeprecationWarning)


def _validate_locators_template(obj: 'RowItem', locators_template: dict):
    if not isinstance(locators_template, dict):
        raise TypeError("{}.locators_template must by <class 'dict'>. "
                        "But was {}".format(obj.__class__.__name__, type(locators_template)))
    for value in locators_template.values():
        if not isinstance(value, tuple):
            raise TypeError("Value of locators_template dict must be <class 'tuple'>. "
                            "But was {}".format(type(value)))


class RowItem:
    """Represents a single row on a list"""

    def __init__(self, row_number: int = 1) -> None:
        self._locators: Dict[str, tuple] = dict()
        _validate_locators_template(self, self.locators_template)
        self.row_number: int = row_number

    def __repr__(self):
        return '{}(row_number="{}")'.format(self.__class__.__name__, self.row_number)

    @property
    @abc.abstractmethod
    def locators_template(self) -> dict:
        """
        Locators template

        Example:
        locators_template = {
            'last_name': (By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(1)"),
            'first_name': (By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(2)"),
            'email': (By.CSS_SELECTOR, "tr:nth-of-type({row}) td:nth-of-type(3)"),
        }
        """

    def __get__(self, obj, owner):
        self.table = obj.table
        if self.table:
            self.update(self.table)
        return self

    def update(self, table: WebElement):
        for attr_name, locator in self.locators.items():
            try:
                element = table.find_element(*locator)
            except NoSuchElementException:
                element = None
            setattr(self, attr_name, element)
        return self

    @property
    def row_number(self) -> int:
        """Returns row number of the current item"""
        return self.__current_row

    @row_number.setter
    def row_number(self, value: int) -> None:
        self.__current_row = value
        self._update_locators(value)

    def _update_locators(self, row_number: int) -> Dict[str, tuple]:
        self._locators = {k: (v[0], v[1].format(row=row_number))
                          for k, v in self.locators_template.items()}
        return self._locators

    @property
    def locators(self) -> Dict[str, tuple]:
        return self._locators
