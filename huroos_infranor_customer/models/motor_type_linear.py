from odoo import fields, models, api


class MotorLinear(models.Model):
    _name = 'motor.type.linear'
    _description = 'Tipi di Motori Lineari'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
