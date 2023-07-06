from odoo import fields, models


STARTING_YEAR = 2020
YEAR_CREATION_LIMIT = 5


def get_dynamic_year_selection():
    global STARTING_YEAR
    selection = list()
    current_year = fields.date.today().year

    while STARTING_YEAR < current_year + YEAR_CREATION_LIMIT:
        selection.append((f'{STARTING_YEAR}', f'{STARTING_YEAR}'))
        STARTING_YEAR += 1

    return selection


class ResPartnerBudget(models.Model):
    _name = "res.partner.budget"
    _description = "Budget per i contatti"
    _order = "partner_id, year desc"

    year = fields.Selection(
        string="Anno",
        selection=get_dynamic_year_selection(),
        default=str(fields.date.today().year),
        required=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cliente",
        domain=[('parent_id', '=', False)],
        required=True
    )
    amount = fields.Monetary(
        string="Budget",
        currency_field="currency_id",
        required=True
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Valuta",
        default=lambda self: self.env.company.currency_id.id
    )

    _sql_constraints = [
        ("unique_year", "UNIQUE(partner_id, year)", "Impossibile avere più budget per un cliente nello stesso anno.")
    ]
