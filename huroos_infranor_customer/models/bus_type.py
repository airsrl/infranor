from odoo import fields, models, api


class BusType(models.Model):
    _name = 'bus.type'
    _description = 'Tipi di Bus'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
