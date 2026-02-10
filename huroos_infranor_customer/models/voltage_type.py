from odoo import fields, models, api


class VoltageType(models.Model):
    _name = 'voltage.type'
    _description = 'Tipi di Voltaggio'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
