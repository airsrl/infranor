from odoo import fields, models, api


class FeedbackType(models.Model):
    _name = 'feedback.type'
    _description = 'Tipi di Feedback'

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', f'Questo nome esiste già per {_description}!')
    ]
