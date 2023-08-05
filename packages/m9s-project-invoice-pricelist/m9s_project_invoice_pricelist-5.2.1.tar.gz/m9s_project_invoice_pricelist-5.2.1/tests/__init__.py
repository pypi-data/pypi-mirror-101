# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.project_invoice_pricelist.tests.test_project_invoice_pricelist import suite
except ImportError:
    from .test_project_invoice_pricelist import suite

__all__ = ['suite']
