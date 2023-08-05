# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'

    @classmethod
    def postprocess_invoices(cls, invoices):
        pool = Pool()
        TimeSheetLine = pool.get('timesheet.line')
        Date = pool.get('ir.date')

        today = Date.today()
        invoices = super(Work, cls).postprocess_invoices(invoices)
        for invoice in invoices:
            time_of_supply_start = today
            time_of_supply_end = None
            timesheet_lines = TimeSheetLine.search([
                ('invoice_line', 'in', [l.id for l in invoice.lines]),
                ])
            for line in timesheet_lines:
                if line.date < time_of_supply_start:
                    time_of_supply_start = line.date
                if time_of_supply_end is None:
                    time_of_supply_end = time_of_supply_start
                elif line.date > time_of_supply_end:
                    time_of_supply_end = line.date
            invoice.time_of_supply_start = time_of_supply_start
            invoice.time_of_supply_end = time_of_supply_end
            invoice.save()
        return invoices
