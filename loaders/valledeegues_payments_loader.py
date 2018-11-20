# -*- coding: UTF-8 -*-
from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget

payments_mapping = {
    'default': {'fc_code': None, 'date': 2, 'payee': 4, 'description': 7, 'amount': 5},
}


class PaymentsCsvMapper:
    def __init__(self, year):
        mapping = payments_mapping.get(str(year))

        if not mapping:
            mapping = payments_mapping.get('default')

        self.fc_code = mapping.get('fc_code')
        self.date = mapping.get('date')
        self.payee = mapping.get('payee')
        self.description = mapping.get('description')
        self.amount = mapping.get('amount')


class ValledeeguesPaymentsLoader(PaymentsLoader):
    # Parse an input line into fields
    def parse_item(self, budget, line):
        # Mapper
        mapper = PaymentsCsvMapper(budget.year)

        # We don't get functional codes
        policy = None

        # We got an iso date or nothing
        date = line[mapper.date] if mapper.date else None

        # Payee data
        payee = line[mapper.payee].strip()

        # We don't get any anonymized entries
        anonymized = False

        # Description
        description = line[mapper.description].strip()

        # Amount
        amount = line[mapper.amount]
        amount = self._read_english_number(amount)

        return {
            'area': policy,
            'programme': None,
            'ic_code': None,
            'fc_code': None,
            'ec_code': None,
            'date': date,
            'payee': payee,
            'anonymized': anonymized,
            'description': description,
            'amount': amount
        }
