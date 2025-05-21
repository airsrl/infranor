from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    price = fields.Float(string="Prezzo")