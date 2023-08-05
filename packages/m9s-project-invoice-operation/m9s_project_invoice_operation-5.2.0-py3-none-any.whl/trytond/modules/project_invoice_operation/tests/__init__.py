# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.project_invoice_operation.tests.test_project_invoice_operation import suite
except ImportError:
    from .test_project_invoice_operation import suite

__all__ = ['suite']
