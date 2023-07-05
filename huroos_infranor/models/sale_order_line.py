from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    x_studio_date_prevue = fields.Date(string="Data prevista")

    commitment_date = fields.Datetime(related="order_id.commitment_date")
