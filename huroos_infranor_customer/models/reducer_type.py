from odoo import fields, models, api


class ReducerType(models.Model):
    _name = 'reducer.type'
    _description = 'Tipi di Riduttori'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
