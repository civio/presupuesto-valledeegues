# -*- coding: UTF-8 -*-
from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget

import re


payments_mapping = {
    'default': {'fc_code': 1, 'date': 3, 'payee': 4, 'description': 7, 'amount': 8},
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

        # We got the functional code
        fc_code = line[mapper.fc_code]

        # first two digits of the functional code make the policy id
        policy_id = fc_code[:2]

        # but what we want as area is the policy description
        policy = Budget.objects.get_all_descriptions(budget.entity)['functional'][policy_id]

        # We got an iso date or nothing
        date = line[mapper.date].strip()
        date = date if date else None

        # We got three consecutive fields with payee data
        payee_data = line[mapper.payee:mapper.payee+3]
        payee = ' '.join([p.strip() for p in payee_data]).strip()

        # remove commas
        payee = payee.replace(', ', ' ').replace(',', ' ')

        # normalize company types
        payee = re.sub(r' S\.L$', ' S.L.', payee)
        payee = re.sub(r' S\.L[^\.]', ' S.L.', payee)
        payee = re.sub(r' SL$', ' S.L.', payee)
        payee = re.sub(r' S\.I$', ' S.I.', payee)
        payee = re.sub(r' SLL$', ' S.L.L.', payee)
        payee = re.sub(r' SLL-', ' S.L.L.-', payee)
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
        payee = re.sub(r' UTE', ' U.T.E.', payee)
        payee = re.sub(r'UTE ', 'U.T.E. ', payee)
        payee = re.sub(r' PLC$', ' P.L.C.', payee)

        # normalize typos
        payee = re.sub('IRAOLA ARTETA', 'IRAOLA-ARTETA', payee)
        payee = re.sub(r'^IRAOLA$', 'IRAOLA-ARTETA S.L.', payee)
        payee = re.sub(r'^MEDIA MARKT CORDOVILLA$', 'MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COPUTER S.A.', payee)
        payee = re.sub(r'^MEDIA MARKT CORDOVILLA PAMPLONA VIDEO$', 'MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COPUTER S.A.', payee)
        payee = re.sub(r'^MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COPUTER S\.A\.$', 'MEDIA MARKT CORDOVILLA-PAMPLONA VIDEO-TV HIFI-COMPUTER S.A.', payee)
        payee = re.sub('SEGURIDAD SISTEMAS NAVARRA S.A.', 'SEGURIDAD SISTEMAS NAVARRA S.L.', payee)
        payee = re.sub('UNIVERSIDAD SOCIEDAD', 'UNIVERSIDAD-SOCIEDAD', payee)
        payee = re.sub('FORESNA ZURGAIA', 'FORESNA-ZURGAIA', payee)
        payee = re.sub('LABORAL RUIZ PIQUER', 'LABORAL RUIZ-PIQUER', payee)
        payee = re.sub(r'ASESORIA LABORAL RUIZ$', 'ASESORIA LABORAL RUIZ-PIQUER S.L.', payee)
        payee = re.sub(r'S\.L\.\(SERNAMAN\)', 'S.L. (SERNAMAN)', payee)
        payee = re.sub(r'^MUY ILUSTRE COLEGIO DE ABOGADOS DE PAMPL$', 'MUY ILUSTRE COLEGIO DE ABOGADOS DE PAMPLONA', payee)
        payee = re.sub(r'^COMUNIDAD FORAL DE NAVARRA \(CULTURA TURISMO RELACIONES INSTITUCIONALES$', 'COMUNIDAD FORAL DE NAVARRA (CULTURA, TURISMO, RELACIONES INSTITUCIONALES)', payee)
        payee = re.sub(r'\(ZAKARLOA S\.L\.', '(ZAKARLOA S.L.)', payee)
        payee = re.sub(r'SL \(PREFABRICADOS\)', 'S.L. (PREFABRICADOS)', payee)
        payee = re.sub(r'^AROZ$', 'AROZ-BERRI S.A.', payee)
        payee = re.sub(r'^AUTO$', 'AUTO-RECAMBIOS ATLANTIC S.L.', payee)
        payee = re.sub(r'^BAG$', 'BAG-DISTRIBUCIONES PUBLICITARIAS S.L.', payee)
        payee = re.sub('BAG- DISTRIBUCIONES', 'BAG-DISTRIBUCIONES', payee)
        payee = re.sub(r'^EDUCACONTINUUM S\.L\.L\.$', 'EDUCACONTINUUM S.L.L.-AGINTZARI S.COOP DE INICIATIVA SOCIAL U.T.E.', payee)
        payee = re.sub(r'^ENTIDAD CONSERVACION P\. IND\. EG.ES SEC$', u'ENTIDAD CONSERVACION P. IND. EGÜES SEC-A', payee)
        payee = re.sub(r'S\.A\.DE', 'S.A. DE', payee)
        payee = re.sub(r'^IPAR$', 'IPAR-ETXE S.I.', payee)
        payee = re.sub(r'^MURGIBE$', 'MURGIBE S.L.', payee)
        payee = re.sub('RADIOPOPULAR', 'RADIO POPULAR', payee)
        payee = re.sub(r'^RADIO POPULAR S\.A\.$', 'RADIO POPULAR S.A. - COPE', payee)
        payee = re.sub(r'^ROTULOS LAVIN\.$', 'ROTULOS LAVIN', payee)
        payee = re.sub(r'^SOCIEDAD ESTATAL DE CORREOS Y TELEGRAFOS S\.A\.$', 'CORREOS Y TELEGRAFOS', payee)
        payee = re.sub(r'^VIVEROS VALDORBA ECHAPARE GONZALEZ CESAR Y LEZAUN INDURAIN MARIA PILAR$', 'VIVEROS VALDORBA', payee)
        payee = re.sub(r'^ALBERO MAULEON ALFONSO Y IBAÑEZ MARIA ARANZAZU$', 'ALBERO MAULEON ALFONSO E IBAÑEZ CELAYETA MARIA ARANZAZU', payee)
        payee = re.sub('M&INGENEIERIA', 'M&M INGENIERIA', payee)

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
