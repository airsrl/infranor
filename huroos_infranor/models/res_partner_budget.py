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
        currency_field="currency_id"
    )
    budget_progress = fields.Float(
        string="Budget rimanente",
        compute="_compute_budget_progress"
    )
    remaining_budget = fields.Monetary(
        string="Budget rimanente",
        currency_field="currency_id",
        compute="_compute_budget_progress"
    )
    sales_amount = fields.Monetary(
        string="Vendite",
        currency_field="currency_id",
        compute="_compute_sales_amount"
    )
    invoiced_amount = fields.Monetary(
        string="Fatturato",
        currency_field="currency_id",
        compute="_compute_amount_invoiced"
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Valuta",
        default=lambda self: self.env.company.currency_id.id
    )
    sale_person_id = fields.Many2one(
        comodel_name="res.users",
        string="Addetto vendite",
        related="partner_id.user_id",
        store=True
    )
    region_id = fields.Many2one(
        comodel_name="res.country.region",
        string="Regione",
        related="partner_id.region_id",
        store=True
    )

    _sql_constraints = [
        ("unique_year", "UNIQUE(partner_id, year)", "Impossibile avere più budget per un cliente nello stesso anno.")
    ]

    @api.depends('partner_id.sale_order_ids')
    def _compute_sales_amount(self):
        """Calcola le vendite totali di ogni anno del relativo partner"""
        for record in self:
            record.sales_amount = 0

            # Ordini dell'anno selezionato
            orders_by_year = record.partner_id.sale_order_ids.filtered(
                lambda sale: sale.state == 'sale'
                and fields.datetime(int(record.year), 1, 1, 0, 0, 0) <= sale.date_order <= fields.datetime(int(record.year), 12, 31, 23, 59, 59)
            )

            for order in orders_by_year:
                record.sales_amount += order.amount_total

    @api.depends('partner_id.invoice_ids')
    def _compute_amount_invoiced(self):
        """Calcola fatturato totale di ogni anno del relativo partner"""
        for record in self:
            record.invoiced_amount = 0

            # Fatture dell'anno selezionato
            invoices = record.partner_id.invoice_ids.filtered(
                lambda move: move.state not in ('draft', 'cancel')
                and move.move_type in ('out_invoice', 'out_refund')
                and fields.date(int(record.year), 1, 1) <= move.invoice_date <= fields.date(int(record.year), 12, 31)
            )

            for inv in invoices:
                record.invoiced_amount += inv.amount_total

    @api.depends('amount', 'invoiced_amount')
    def _compute_budget_progress(self):
        for record in self:
            record.budget_progress = 0
            record.remaining_budget = 0

            if record.amount != 0:
                record.budget_progress = (record.invoiced_amount / record.amount) * 100
                record.remaining_budget = record.amount - record.invoiced_amount

