from odoo import fields, models, api


class MotorRotary(models.Model):
    _name = 'motor.type.rotary'
    _description = 'Tipi di Motori Rotativi'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
