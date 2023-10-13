from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_to_deliver = fields.Float(compute="_compute_qty_delivery", store=True, readonly=True)

    @api.depends('product_qty', 'qty_received')
    def _compute_qty_delivery(self):
        for line in self:
            line.qty_to_deliver = line.product_qty - line.qty_received