from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    revenue = fields.Float(string="Fatturato")
    potential = fields.Float(string="Potenziale")

    # Motors
    motors_main_competitors = fields.Text(string="Motori - Competitor principali")
    motors_rotary_id = fields.Many2one(string="Motori - Tipi Rotativi usati", comodel_name='motor.type.rotary')
    motors_linear_id = fields.Many2one(string="Motori - Tipi Lineari usati", comodel_name='motor.type.linear')
    motors_use_tubular = fields.Boolean(string="Motori - Tubolari?")
    motors_feedback_id = fields.Many2one(string="Motori - Feedback gestibili", comodel_name='feedback.type')
    motors_protection_ids = fields.Many2many(string="Motori - Livelli di protezione", comodel_name='protection.level')
    motors_voltage_id = fields.Many2one(string="Motori - Tensioni supportate", comodel_name='voltage.type')
    motors_integrated_electronics = fields.Boolean(string="Motori - Elettronica integrata?")
    motors_integrated_electronics_voltage = fields.Char(string="Motori - Tensione di alimentazione elettronica integrata")

    # BUS DI CAMPO
    bus_ids = fields.Many2many(string="Bus di campo usato su motori/azionamenti", comodel_name='bus.type')

    # Riduttori
    reducer_competitors = fields.Text(string="Riduttori - Competitor principali")
    reducer_type_ids = fields.Many2many(string="Riduttori - Tipi usati", comodel_name='reducer.type')

    # Azionamenti
    drives_competitors = fields.Text(string="Azionamenti - Competitor principali")
    drives_voltage_ids = fields.Many2many(string="Azionamenti - Tensioni supportate", comodel_name='voltage.type')
    drives_feedback_ids = fields.Many2many(string="Azionamenti - Feedback gestibili", comodel_name='feedback.type')
    drives_bus_id = fields.Many2one(string="Azionamenti - Bus compatibili", comodel_name='bus.type')
    drives_security_ids = fields.Many2many(string="Azionamenti - Funzioni di sicurezza disponibili", comodel_name='security.function')

    # Commerciali
    commercial_date_meet = fields.Date(string="Commerciali - Data visita/chiamata")
    commercial_note = fields.Text(string="Commerciali - Note associate")
    commercial_activity_ids = fields.One2many(string="Commerciali - Cronologia attività", comodel_name='commercial.activity.line', inverse_name='partner_id')

