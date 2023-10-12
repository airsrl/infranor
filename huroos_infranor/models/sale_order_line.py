from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    x_studio_date_prevue = fields.Date(string = "Data prevista",)
    commitment_date = fields.Datetime(related="order_id.commitment_date")
    previous_qty_invoiced = fields.Float()

    #_compute_qty_to_invoice
    #_compute_invoice_status

    #def compute_previous_invoiced(self):

    qty_to_deliver = fields.Float(compute="_compute_qty_to_deliver", store=True, readonly=True)

    @api.depends('product_uom_qty', 'qty_delivered')
    def _compute_qty_to_deliver(self):
        for line in self:
            line.qty_to_deliver = line.product_uom_qty - line.qty_delivered

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity')
    def _compute_qty_invoiced(self):
        """
        Aggiunta somma quantità fatturata tramite software esterno e generazione xml
        da Studio commercialista. Questa funzione ereditata non cambia la logica di Odoo
        chiama la super ed aggiunge semplicemente un eventuale qty inserita in un campo secondario.
        """
        res = super(SaleOrder, self)._compute_qty_invoiced()

        for line in self:
            qty_invoiced = 0.0
            for invoice_line in line._get_invoice_lines():
                if invoice_line.move_id.state != 'cancel' or invoice_line.move_id.payment_state == 'invoicing_legacy':
                    if invoice_line.move_id.move_type == 'out_invoice':
                        qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
                    elif invoice_line.move_id.move_type == 'out_refund':
                        qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)

            line.qty_invoiced = qty_invoiced + line.previous_qty_invoiced

        return res