from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    position = fields.Char(string="Posizione")
