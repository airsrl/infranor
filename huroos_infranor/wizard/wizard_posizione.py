from odoo import fields, models, api


class PosizioneWizard(models.TransientModel):
    _name = 'posizione.wizard'

    product_id = fields.Many2one('product.product')
    new_position = fields.Char()
    def edit_posizione(self):
        self.product_id.position = self.new_position

