from odoo import models


class StockDeliveryNoteCreateWizard(models.TransientModel):
    _inherit = "stock.delivery.note.create.wizard"

    def confirm(self):
        res = super(StockDeliveryNoteCreateWizard, self).confirm()

        sale_order_ids = self.mapped("selected_picking_ids.sale_id")

        if len(sale_order_ids) == 1 and len(self.selected_picking_ids.delivery_note_id) == 1:
            delivery_note = self.selected_picking_ids.delivery_note_id

            # Compilazione automatica campi custom alla creazione del DDT
            delivery_note.order_ref = sale_order_ids.origin
            delivery_note.confirm_number = sale_order_ids.name

            # Aggiunta delle righe di nota del SO
            note_lines = sale_order_ids.order_line.filtered(lambda l: l.display_type == "line_note")
            new_lines = list()
            for line in note_lines:
                line_vals = {
                    'name': line.name,
                    'display_type': "line_note",
                    'sequence': line.sequence
                }
                new_lines.append((0, 0, line_vals))
            delivery_note.write({'line_ids': new_lines})

        return res
