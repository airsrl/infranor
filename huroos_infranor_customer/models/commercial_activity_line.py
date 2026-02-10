from odoo import fields, models, api


class CommercialActivityLine(models.Model):
    _name = 'commercial.activity.line'
    _description = 'Riga di Attività Commerciale'

    description = fields.Text(string="Descrizione")
    sequence = fields.Integer(string="Sequenza")
    partner_id = fields.Many2one(string="Partner", comodel_name='res.partner')
    date = fields.Date(string="Data")
