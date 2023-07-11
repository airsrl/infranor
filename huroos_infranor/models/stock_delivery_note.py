from odoo import fields, models


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    order_ref = fields.Char(
        string="Rif. Ordine",
        groups="huroos_infranor.vat_registries_group"
    )
    confirm_number = fields.Char(
        string="Numero conferma d'ordine",
        groups="huroos_infranor.vat_registries_group"
    )
