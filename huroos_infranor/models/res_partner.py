from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    budget_ids = fields.One2many(
        inverse_name="partner_id",
        comodel_name="res.partner.budget",
        string="Budget cliente",
        groups="huroos_infranor.vat_registries_group"
    )
    current_year_budget = fields.Float(
        string=f"Budget {fields.date.today().year}",
        compute="_compute_current_year_budget",
        groups="huroos_infranor.vat_registries_group"
    )
    carrier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vettore",
        groups="huroos_infranor.vat_registries_group"
    )

    @api.depends('budget_ids')
    def _compute_current_year_budget(self):
        current_year = fields.date.today().year
        for partner in self:
            partner.current_year_budget = partner.budget_ids.filtered(lambda bdg: bdg.year == str(current_year)).amount


