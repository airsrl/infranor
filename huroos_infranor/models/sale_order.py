from odoo import api, fields, models
from markupsafe import Markup
import datetime


def filter_dates(date, operator, value):
    operator = str(operator)
    if value:
        value = datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
    if date:
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
        elif operator == '=':
            return date == value
        elif operator == 'in':
            return date in value
    else:
        return False


class SaleOrder(models.Model):
    _inherit = "sale.order"

    expected_date = fields.Datetime(
        string="Expected Date",
        compute='_compute_expected_date', store=False,  # Note: can not be stored since depends on today()
        help="Delivery date you can promise to the customer, computed from the minimum lead time of the order lines.",
        search="_search_expected_date")

    offer_number = fields.Char(
        help="Campo tecnico per visualizzare sul report un suffisso diverso tra Preventivo e Ordine",
        compute="_compute_offer_number",
        groups="huroos_infranor.vat_registries_group"
    )

    @api.depends('state')
    def _compute_offer_number(self):
        for order in self:
            if order.state == 'draft':
                number = "P"
                for letter in order.name:
                    if letter.isdigit():
                        number += letter
                order.offer_number = number
            else:
                order.offer_number = False

    def _search_expected_date(self, operator, value):
        orders = self.search([]).filtered(lambda x : filter_dates(x.expected_date, operator, value))
        return [('id', 'in', [x.id for x in orders] if orders else False)]

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        new_notes = Markup(f"<p><h3><strong>Rif. Odoo: {self.name}</strong></h3></p>")
        if self.origin:
            new_notes += Markup(f"<p><h3><strong>Rif. Cliente: {self.origin}</strong></h3></p>")

        if invoice_vals.get('narration', False):
            new_notes += invoice_vals['narration']

        invoice_vals['narration'] = new_notes

        return invoice_vals
