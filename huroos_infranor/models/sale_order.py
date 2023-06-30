from odoo import fields, models
import datetime

def filter_dates(date, operator, value):
    operator = str(operator)
    value = datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
    if operator == '>':
        return date > value
    elif operator == '>=':
        return date >= value
    elif operator == '<':
        return date < value
    elif operator == '<=':
        return date <= value
    elif operator == '!=':
        return date != value
    elif operator == 'in':
        return date in value

class SaleOrder(models.Model):
    _inherit = "sale.order"

    expected_date = fields.Datetime(
        string="Expected Date",
        compute='_compute_expected_date', store=False,  # Note: can not be stored since depends on today()
        help="Delivery date you can promise to the customer, computed from the minimum lead time of the order lines.",
        search = "_search_expected_date")

    def _search_expected_date(self, operator, value):
        orders = self.search([]).filtered(lambda x : filter_dates(x.expected_date, operator, value))
        return [('id', 'in', [x.id for x in orders] if orders else False)]