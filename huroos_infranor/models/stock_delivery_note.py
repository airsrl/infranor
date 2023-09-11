from odoo import api, fields, models


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

    @api.onchange('partner_id')
    def _get_default_carrier(self):
        if self.partner_id and self.partner_id.carrier_id:
            self.carrier_id = self.partner_id.carrier_id

