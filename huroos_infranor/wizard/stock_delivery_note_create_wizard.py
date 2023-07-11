from odoo import models


class StockDeliveryNoteCreateWizard(models.TransientModel):
    _inherit = "stock.delivery.note.create.wizard"

    def confirm(self):
        res = super(StockDeliveryNoteCreateWizard, self).confirm()

        sale_order_ids = self.mapped("selected_picking_ids.sale_id")

        if len(sale_order_ids) == 1 and len(self.selected_picking_ids.delivery_note_id) == 1:
            self.selected_picking_ids.delivery_note_id.order_ref = sale_order_ids.origin
            self.selected_picking_ids.delivery_note_id.note = sale_order_ids.note
            self.selected_picking_ids.delivery_note_id.confirm_number = sale_order_ids.name

        return res
