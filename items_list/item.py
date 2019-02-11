class Item:
    """Represents single item in list"""

    def __init__(self, locators_template, item_number):

        self.__locators = {}
        self.__validate_locators_template(locators_template)
        self.__locators_template = locators_template
        self.__item_number = item_number
        self.update_item_number(item_number)

    def update_item_number(self, item_number):
        self.__item_number = item_number
        self.__locators = {k: v.format(item_num=item_number)
                           for k, v in self.__locators_template.items()}
        return self.__locators

    @property
    def locators(self):
        _locators = dict()
        for item, locator in self.__locators.items():
            locator = locator.split('==')
            _locators[item] = (*locator,)
        return _locators

    def get_item_number(self):
        return self.__item_number

    def __validate_locators_template(self, locators_template):
        assert isinstance(locators_template, dict)
        for values in locators_template.values():
            assert '==' in values
