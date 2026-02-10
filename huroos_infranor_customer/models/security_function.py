from odoo import fields, models, api


class SecurityFunction(models.Model):
    _name = 'security.function'
    _description = 'Funzioni di Sicurezza'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
