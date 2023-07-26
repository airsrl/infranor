from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    budget_ids = fields.One2many(
        inverse_name="partner_id",
        comodel_name="res.partner.budget",
        string="Budget cliente",
        groups="huroos_infranor.vat_registries_group"
    )
    carrier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vettore",
        groups="huroos_infranor.vat_registries_group"
    )


