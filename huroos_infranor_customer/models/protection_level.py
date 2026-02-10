from odoo import fields, models, api


class ProtectionLevel(models.Model):
    _name = 'protection.level'
    _description = 'Livelli di Protezione'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
