# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import work

__all__ = ['register']


def register():
    Pool.register(
        work.Work,
        module='project_invoice_pricelist', type_='model')
