from odoo import api, fields, models
from odoo.exceptions import ValidationError


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


def get_invoices_in_period(date_start: fields.date, date_end: fields.date, invoice_ids):
    """
    :param date_start: Data di inizio
    :param date_end: Data di fine
    :param invoice_ids: account.move recordset

    Filtra le fatture di un recordset da date_start a date_end
    """
    return invoice_ids.filtered(
        lambda move: move.state not in ('draft', 'cancel')
        and move.move_type in ('out_invoice', 'out_refund')
        and date_start <= move.invoice_date <= date_end
    )


class ResPartnerBudget(models.Model):
    _name = "res.partner.budget"
    _description = "Budget per i contatti"
    _order = "partner_id, year DESC"

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
    # ---------- CAMPI BUDGET ---------- #
    budget_amount = fields.Monetary(
        string="Budget",
        currency_field="currency_id"
    )
    budget_progress = fields.Float(
        string="Progresso budget",
        compute="_compute_budget_progress"
    )
    remaining_budget = fields.Monetary(
        string="Budget rimanente",
        currency_field="currency_id",
        compute="_compute_budget_progress"
    )
    # ---------- CAMPI FATTURATO ---------- #
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
    current_year_invoiced_amount = fields.Float(
        string="Fatt. anno corrente",
        compute="_compute_current_year_invoiced_amount",
        store=True,
        help="Campo tecnico al momento non utilizzato. Serve a contenere il fatturato dell'anno solare corrente."
    )
    invoiced_amount_date = fields.Monetary(
        string="Fatt. alla data",
        currency_field="currency_id",
        compute="_compute_invoiced_amount_date"
    )
    invoiced_amount_date_previous_year = fields.Monetary(
        string="Fatt. alla data anno prec.",
        currency_field="currency_id",
        compute="_compute_invoiced_amount_date",
        help="Fatturato alla data (anno precedente)"
    )
    reference_date = fields.Date(
        string="Data di riferimento",
        default=fields.date.today(),
        help="Campo che comanda 'Fatturato alla data' e 'Fatturato anno precedente', per avere un confronto"
             "tra fatturati in una data specifica."
    )

    # ---------- CONSTRAINS ---------- #
    _sql_constraints = [
        ("unique_year", "UNIQUE(partner_id, year)", "Impossibile avere più budget per un cliente nello stesso anno.")
    ]

    @api.constrains('reference_date')
    def _check_reference_date(self):
        for record in self:
            if not fields.date(int(record.year), 1, 1) <= record.reference_date <= fields.date(int(record.year), 12, 31):
                raise ValidationError(f"Per favore inserisci una data compresa nell'anno del budget preso in esame ({record.year}).")

    # ---------- COMPUTE METHODS ---------- #
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
            invoices = get_invoices_in_period(
                date_start=fields.date(int(record.year), 1, 1),
                date_end=fields.date(int(record.year), 12, 31),
                invoice_ids=record.partner_id.invoice_ids
            )
            # Sommo l'imponibile di tutte le fatture
            for inv in invoices:
                record.invoiced_amount += inv.amount_untaxed

    @api.depends('budget_amount', 'invoiced_amount')
    def _compute_budget_progress(self):
        """Calcolo del budget rimanente e della percentuale di progresso"""
        for record in self:
            record.budget_progress = 0
            record.remaining_budget = 0

            if record.budget_amount != 0:
                record.budget_progress = (record.invoiced_amount / record.budget_amount) * 100
                record.remaining_budget = record.budget_amount - record.invoiced_amount

    @api.depends('partner_id.budget_ids')
    def _compute_current_year_invoiced_amount(self):
        """Calcolo del fatturato dell'anno corrente"""
        for record in self:
            current_year_budget_obj = record.partner_id.budget_ids.filtered(lambda bdg: bdg.year == str(fields.date.today().year))

            if not current_year_budget_obj or record != current_year_budget_obj:
                record.current_year_invoiced_amount = 0
            else:
                record.current_year_invoiced_amount = current_year_budget_obj.invoiced_amount

    @api.depends('partner_id.invoice_ids', 'reference_date')
    def _compute_invoiced_amount_date(self):
        """Calcolo fatturati alla data (anno corrente e anno precedente)"""
        for record in self:

            record.invoiced_amount_date = 0
            record.invoiced_amount_date_previous_year = 0

            if not record.reference_date:
                continue

            # Fatture anno selezionato
            current_year_invoices = get_invoices_in_period(
                date_start=fields.date(int(record.year), 1, 1),
                date_end=record.reference_date,
                invoice_ids=record.partner_id.invoice_ids
            )
            # Sommo l'imponibile di tutte le fatture
            for inv in current_year_invoices:
                record.invoiced_amount_date += inv.amount_untaxed

            try:
                previous_year_reference_date = fields.date(
                    year=record.reference_date.year - 1,
                    month=record.reference_date.month,
                    day=record.reference_date.day
                )

            except Exception as ex:
                raise ValidationError(f"Errore: {ex}")

            else:
                # Fatture anno precedente
                previous_year_invoices = get_invoices_in_period(
                    date_start=fields.date(int(record.year) - 1, 1, 1),
                    date_end=previous_year_reference_date,
                    invoice_ids=record.partner_id.invoice_ids
                )
                # Sommo l'imponibile di tutte le fatture
                for inv in previous_year_invoices:
                    record.invoiced_amount_date_previous_year += inv.amount_untaxed
