from odoo import fields, models, api


class StockQuant(models.Model):
    _inherit = "stock.quant"

    price = fields.Float(string="Prezzo")

    @api.model
    def _get_inventory_fields_create(self):
        res = super(StockQuant, self)._get_inventory_fields_create()
        if res:
            res = res + ['price']
        return res