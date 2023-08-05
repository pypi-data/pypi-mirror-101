# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountInvoiceTimeSupplyTestCase(ModuleTestCase):
    'Test Account Invoice Time Supply module'
    module = 'account_invoice_time_supply'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoiceTimeSupplyTestCase))
    return suite
