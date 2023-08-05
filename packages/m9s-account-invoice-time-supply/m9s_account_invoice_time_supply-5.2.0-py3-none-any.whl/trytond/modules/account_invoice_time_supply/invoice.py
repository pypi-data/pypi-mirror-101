# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

from trytond.modules.account_invoice.invoice import _STATES, _DEPENDS


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    time_of_supply_start = fields.Date('Time of Supply Start', states=_STATES,
        depends=_DEPENDS)
    time_of_supply_end = fields.Date('Time of Supply End', states=_STATES,
        depends=_DEPENDS)

    def _credit(self):
        res = super(Invoice, self)._credit()
        res['time_of_supply_start'] = self.time_of_supply_start
        res['time_of_supply_end'] = self.time_of_supply_end
        return res
