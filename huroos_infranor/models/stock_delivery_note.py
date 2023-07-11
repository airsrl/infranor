from odoo import fields, models


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    order_ref = fields.Char(
        string="Rif. Ordine",
        groups="huroos_infranor.vat_registries_group"
    )
