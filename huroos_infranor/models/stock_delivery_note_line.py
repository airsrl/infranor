from odoo import api, fields, models


class StockDeliveryNoteLine(models.Model):
    _inherit = "stock.delivery.note.line"

    @api.model
    def _get_serial_default(self):
        return {'name': 'hello'}

    serial_ids = fields.Many2many(
        "stock.lot",
        string="Numeri di Serie",
        default=_get_serial_default
    )

    # @api.model
    # def _prepare_detail_lines(self, moves):
    #     lines = super(StockDeliveryNoteLine, self)._prepare_detail_lines(moves)
    #     for line in lines:
    #         if 'move_id' in line and line['move_id']:
    #             move_id = self.env["stock.move"].browse(line['move_id'])
    #             line['serial_ids'] = move_id.lot_ids.ids
    #
    #     return lines