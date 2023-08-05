# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import invoice

__all__ = ['register']


def register():
    Pool.register(
        module='project_invoice_operation', type_='model')
    Pool.register(
        module='project_invoice_operation', type_='wizard')
    Pool.register(
        invoice.OperationReport,
        module='project_invoice_operation', type_='report')
