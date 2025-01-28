from odoo import models, fields

class Periodo(models.Model):
    _name = 'proyecto_odoo.periodo'
    _description = 'Modelo de Periodo'

    name = fields.Char(string='Nombre Periodo:', required=True)