from odoo import api, fields, models


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
    sales_amount = fields.Monetary(
        string="Vendite totali",
        currency_field="currency_id",
        compute="_compute_sales_amount"
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Valuta",
        default=lambda self: self.env.company.currency_id.id
    )

    _sql_constraints = [
        ("unique_year", "UNIQUE(partner_id, year)", "Impossibile avere più budget per un cliente nello stesso anno.")
    ]

    @api.depends('partner_id.sale_order_count')
    def _compute_sales_amount(self):
        """Calcola le vendite totali di ogni anno del relativo partner"""
        for record in self:
            record.sales_amount = 0
            domain = [
                ('state', '=', 'sale'),
                ('partner_id', '=', record.partner_id.id),
                ('date_order', '>=', f'{record.year}-01-01'),
                ('date_order', '<=', f'{record.year}-12-31')
            ]
            orders_by_year = self.env['sale.order'].search(domain)

            for order in orders_by_year:
                record.sales_amount += order.amount_total
