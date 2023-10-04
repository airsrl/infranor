
from collections import defaultdict
import copy

from odoo import api, models
from odoo.tools import float_compare, float_is_zero, format_date, float_round

class ReplenishmentReport(models.AbstractModel):
    _inherit = 'report.stock.report_product_product_replenishment'

    def _get_date_move(self,move_in=False,move_out=False):
        if move_out:
            if move_out.sale_line_id:
                if move_out.sale_line_id.x_studio_date_prevue:
                    return move_out.sale_line_id.x_studio_date_prevue
                elif move_out.sale_line_id.order_id.commitment_date:
                    return move_out.sale_line_id.order_id.commitment_date
            return move_out.date
        elif move_in:
            if move_in.purchase_line_id:
                if move_in.purchase_line_id.date_planned:
                    return move_in.purchase_line_id.date_planned
            return move_in.date


    def _prepare_report_line(self, quantity, move_out=None, move_in=None, replenishment_filled=True, product=False, reservation=False):
        product = product or (move_out.product_id if move_out else move_in.product_id)
        is_late = move_out.date < move_in.date if (move_out and move_in) else False

        move_to_match_ids = self.env.context.get('move_to_match_ids') or []
        move_in_id = move_in.id if move_in else None
        move_out_id = move_out.id if move_out else None
        return {
            'document_in': move_in._get_source_document() if move_in else False,
            'document_out': move_out._get_source_document() if move_out else False,
            'product': {
                'id': product.id,
                'display_name': product.display_name
            },
            'replenishment_filled': replenishment_filled,
            'uom_id': product.uom_id,
            'receipt_date': format_date(self.env, self._get_date_move(move_in=move_in)) if move_in else False,
            'delivery_date': format_date(self.env, self._get_date_move(move_out=move_out)) if move_out else False,
            'is_late': is_late,
            'quantity': float_round(quantity, precision_rounding=product.uom_id.rounding),
            'move_out': move_out,
            'move_in': move_in,
            'reservation': reservation,
            'is_matched': any(move_id in [move_in_id, move_out_id] for move_id in move_to_match_ids),
        }
