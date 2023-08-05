# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval, Not, Equal, Or, Bool


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    price_list = fields.Many2One('product.price_list', 'Price List',
        domain=[('company', '=', Eval('company'))],
        states={
            'readonly': Not(Equal(Eval('state'), 'opened')),
            },
        depends=['state', 'company'],
        help='Use the first pricelist found in following precedence:\n\n'
        '- Pricelist of the task\n'
        '- Pricelist of the parent project\n'
        '- Pricelist of the party')
    price_list_used = fields.Function(fields.Many2One('product.price_list',
            'Price List Used'), 'get_price_list')

    def get_price_list(self, name):
        if self.price_list:
            return self.price_list
        parent_project = self.__class__.search([
                ('parent', 'parent_of', [self.id]),
                ('parent', '=', None),
                ])
        if parent_project:
            project = parent_project[0]
            if project.price_list:
                return project.price_list
            elif project.party:
                return project.party.sale_price_list
        elif self.party:
            return self.party.sale_price_list

    @fields.depends('party')
    def on_change_party(self):
        self.price_list = None
        if self.party and self.party.sale_price_list:
            self.price_list = self.party.sale_price_list

    def _group_lines_to_invoice_key(self, line):
        key = super(Work, self)._group_lines_to_invoice_key(line)
        key += (('price_list', line['price_list']),)
        return key

    def _add_price_list_to_lines(self, lines):
        for line in lines:
            line['price_list'] = self.price_list_used
        return lines

    def _get_lines_to_invoice_effort(self):
        lines = super(Work, self)._get_lines_to_invoice_effort()
        return self._add_price_list_to_lines(lines)

    def _get_lines_to_invoice_progress(self):
        lines = super(Work, self)._get_lines_to_invoice_progress()
        return self._add_price_list_to_lines(lines)

    def _get_lines_to_invoice_timesheet(self):
        lines = super(Work, self)._get_lines_to_invoice_timesheet()
        return self._add_price_list_to_lines(lines)

    def _get_lines_to_invoice_hours(self):
        lines = super(Work, self)._get_lines_to_invoice_hours()
        return self._add_price_list_to_lines(lines)

    def _get_invoice_line(self, key, invoice, lines):
        pool = Pool()
        Product = pool.get('product.product')

        invoice_line = super(Work, self)._get_invoice_line(
            key, invoice, lines)

        pricelist = key['price_list']
        if pricelist:
            with Transaction().set_context({
                    'price_list': pricelist.id,
                    'customer': self.party.id,
                    }):
                prices = Product.get_sale_price([self.product], 0)
                invoice_line.unit_price = prices[self.product.id]
        return invoice_line
