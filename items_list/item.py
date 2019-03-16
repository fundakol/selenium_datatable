class Item:
    """Represents single item in list"""

    def __init__(self, locators_template: dict, item_number: int) -> None:
        self.__locators = {}
        self.__validate_locators_template(locators_template)
        self.__locators_template = locators_template
        self.__item_number = item_number
        self.update_item_number(item_number)

    def update_item_number(self, item_number: int) -> dict:
        self.__item_number = item_number
        self.__locators = {k: v.format(item_num=item_number)
                           for k, v in self.__locators_template.items()}
        return self.__locators

    @property
    def locators(self) -> dict:
        _locators = dict()
        for item, locator in self.__locators.items():
            locator = locator.split('==')
            _locators[item] = (*locator,)
        return _locators

    @property
    def item_number(self) -> int:
        """Returns row number of the current item"""
        return self.__item_number

    def __validate_locators_template(self, locators_template: dict):
        assert isinstance(locators_template, dict)
        for values in locators_template.values():
            assert '==' in values
