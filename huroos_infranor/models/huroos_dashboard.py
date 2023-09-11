from base64 import b64decode

import xlrd

from odoo import api, fields, models


class HuroosDashboard(models.Model):
    _name = 'infranor.huroos.dashboard'

    file = fields.Binary()

    def compute_previous_invoiced(self):
        book = xlrd.open_workbook(file_contents=b64decode(self.file))
        for sheet in book.sheets():
            for row in range(sheet.nrows):
                if row >= 1:
                    row_values = sheet.row_values(row)
                    sale_line_id = int(row_values[0])
                    qty_invoiced = float(row_values[1])

                    obj_sale_line_id = self.env['sale.order.line'].browse(sale_line_id)
                    obj_sale_line_id.write({'previous_qty_invoiced': qty_invoiced})
                    obj_sale_line_id._compute_qty_invoiced()
                    obj_sale_line_id._compute_qty_to_invoice()
                    obj_sale_line_id._compute_invoice_status()