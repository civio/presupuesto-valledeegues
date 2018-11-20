# -*- coding: UTF-8 -*-
from budget_app.loaders import SimpleBudgetLoader

expenses_mapping = {
    'default': {'fc_code': 2, 'full_ec_code': 3, 'description': 4, 'forecast_amount': 7, 'actual_amount': 11},
    '2018': {'fc_code': 2, 'full_ec_code': 3, 'description': 4, 'forecast_amount': 13, 'actual_amount': None    },
}

income_mapping = {
    'default': {'full_ec_code': 1, 'description': 2, 'forecast_amount': 8, 'actual_amount': 10},
    '2018': {'full_ec_code': 2, 'description': 3, 'forecast_amount': 13, 'actual_amount': None},
}


class BudgetCsvMapper:
    def __init__(self, year, is_expense):
        column_mapping = income_mapping

        if is_expense:
            column_mapping = expenses_mapping

        mapping = column_mapping.get(str(year))

        if not mapping:
            mapping = column_mapping.get('default')

        self.ic_code = mapping.get('ic_code')
        self.fc_code = mapping.get('fc_code')
        self.full_ec_code = mapping.get('full_ec_code')
        self.description = mapping.get('description')
        self.forecast_amount = mapping.get('forecast_amount')
        self.actual_amount = mapping.get('actual_amount')


class ValledeeguesBudgetLoader(SimpleBudgetLoader):

    # An artifact of the in2csv conversion of the original XLS files is a trailing '.0', which we remove here
    def clean(self, s):
        return s.split('.')[0]

    # Make year data available in the class and call super
    def load(self, entity, year, path, status):
        self.year = year
        SimpleBudgetLoader.load(self, entity, year, path, status)

    # Parse an input line into fields
    def parse_item(self, filename, line):
        # We ignore non budget lines
        if line[0] is not '1':
            return None

        # Type of data
        is_expense = (filename.find('gastos.csv') != -1)
        is_actual = (filename.find('/ejecucion_') != -1)

        # Mapper
        mapper = BudgetCsvMapper(self.year, is_expense)

        # Institutional code
        # All expenses go to the root node
        ic_code = '000'

        # Economic code
        full_ec_code = line[mapper.full_ec_code].strip()

        # Concepts are the firts three digits from the economic codes
        ec_code = full_ec_code[:3]

        # Item numbers are the last two digits from the economic codes (fourth and fifth digits)
        item_number = full_ec_code[-2:]

        # Description
        description = line[mapper.description].strip()
        description = self._spanish_titlecase(description)

        # Parse amount
        amount = line[mapper.actual_amount if is_actual else mapper.forecast_amount]
        amount = self._parse_amount(amount)

        if is_expense:
            # Functional code
            # We got 5-digit functional codes as input, but we only need the first four
            fc_code = line[mapper.fc_code].strip()
            fc_code = fc_code[:4]

        # Income
        else:
            # Functional code
            # We don't have a functional code in income
            fc_code = None

        return {
            'is_expense': is_expense,
            'is_actual': is_actual,
            'fc_code': fc_code,
            'ec_code': ec_code,
            'ic_code': ic_code,
            'item_number': item_number,
            'description': description,
            'amount': amount
        }
