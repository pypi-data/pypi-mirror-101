# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import invoice
from . import work

__all__ = ['register']


def register():
    Pool.register(
        invoice.Invoice,
        module='account_invoice_time_supply', type_='model')
    Pool.register(
        work.Work,
        module='account_invoice_time_supply', type_='model',
        depends=['project_invoice'])
