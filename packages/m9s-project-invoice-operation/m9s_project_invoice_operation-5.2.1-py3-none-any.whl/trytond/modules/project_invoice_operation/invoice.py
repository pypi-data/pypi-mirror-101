# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime

from trytond.pool import Pool
from trytond.report import Report


class OperationReport(Report):
    __name__ = 'account.invoice.operation_report'

    @classmethod
    def get_context(cls, records, data):
        pool = Pool()
        TimeSheetLine = pool.get('timesheet.line')

        report_context = super(OperationReport, cls).get_context(records, data)

        invoice = records[0]
        timesheet_lines = TimeSheetLine.search([
                ('invoice_line', 'in', [l.id for l in invoice.lines]),
                ], order=[('date', 'ASC')])
        total_duration = sum([l.duration for l in timesheet_lines],
            datetime.timedelta())

        report_context['timesheet_lines'] = timesheet_lines
        report_context['total_duration'] = total_duration
        report_context['format_duration'] = cls.format_duration
        return report_context

    @classmethod
    def format_duration(cls, duration , lang, digits=2, grouping=True,
            monetary=None):
        pool = Pool()
        Lang = pool.get('ir.lang')

        total_seconds = duration.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        #seconds = total_seconds % 60
        duration_hours = hours + minutes / 60
        return Lang.format(lang, '%.' + str(digits) + 'f',
            duration_hours, grouping=grouping, monetary=monetary)
