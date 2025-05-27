# from odoo import models, api
#
#
# class StockMoveLine(models.Model):
#     _inherit = "stock.move.line"
#
#     @api.ondelete(at_uninstall=False)
#     def _unlink_except_done_or_cancel(self):
#         for ml in self:
#             if ml.state in ('done', 'cancel'):
#                 print('You can not delete product moves if the picking is done. You can only correct the done quantities.')