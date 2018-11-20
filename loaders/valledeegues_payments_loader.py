# -*- coding: UTF-8 -*-
from budget_app.loaders import PaymentsLoader
import re


payments_mapping = {
    'default': {'fc_code': None, 'date': 1, 'payee': 3, 'description': 6, 'amount': 4},
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

        # remove commas
        payee = payee.replace(', ', ' ').replace(',', ' ')

        # normalize company types
        payee = re.sub(r' S\.L$', ' S.L.', payee)
        payee = re.sub(r' S\.L[^\.]', ' S.L.', payee)
        payee = re.sub(r' SL$', ' S.L.', payee)
        payee = re.sub(r' S\.I$', ' S.I.', payee)
        payee = re.sub(r' SLL$', ' S.L.L.', payee)
        payee = re.sub(r' SLU$', ' S.L.U.', payee)
        payee = re.sub(r' S\.L\.U$', ' S.L.U.', payee)
        payee = re.sub(r' S\.L\.U[^\.]', ' S.L.U.', payee)
        payee = re.sub(r' SLD$', ' S.L.D.', payee)
        payee = re.sub(r' S\.A$', ' S.A.', payee)
        payee = re.sub(r' S\.A[^\.]', ' S.A.', payee)
        payee = re.sub(r' SA$', ' S.A.', payee)
        payee = re.sub(r' SAU$', ' S.A.U.', payee)
        payee = re.sub(r' SRL$', ' S.R.L.', payee)
        payee = re.sub(r' AG$', ' A.G.', payee)

        # normalize typos
        payee = re.sub('IRAOLA ARTETA', 'IRAOLA-ARTETA', payee)
        payee = re.sub('MEDIA MARKT CORDOVILLA', 'MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COPUTER S.A.', payee)
        payee = re.sub('MEDIA MARKT CORDOVILLA PAMPLONA VIDEO', 'MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COPUTER S.A.D', payee)
        payee = re.sub('MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COPUTER S.A.', 'MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COMPUTER S.A.', payee)
        payee = re.sub('SEGURIDAD SISTEMAS NAVARRA S.A.', 'SEGURIDAD SISTEMAS NAVARRA S.L.', payee)
        payee = re.sub('UNIVERSIDAD SOCIEDAD', 'UNIVERSIDAD-SOCIEDAD', payee)
        payee = re.sub('FORESNA ZURGAIA', 'FORESNA-ZURGAIA', payee)
        payee = re.sub('LABORAL RUIZ PIQUER', 'LABORAL RUIZ-PIQUER', payee)
        payee = re.sub(r'ASESORIA LABORAL RUIZ$', 'ASESORIA LABORAL RUIZ-PIQUER S.L.', payee)

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
