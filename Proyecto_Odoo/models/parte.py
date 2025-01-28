from odoo import models, fields

class Parte(models.Model):
    _name = 'proyecto_odoo.parte'
    _description = 'Modelo de Parte'

    # Identificador único manual
    custom_id = fields.Integer(string='ID:', required=True, help="Identificador único para esta parte. Debe ser único.")

    name = fields.Char(string='Nombre:', required=True)
    tipo = fields.Selection([
        ('Primario', 'Primario'),
        ('Secundario', 'Secundario'),
        ('Terciario', 'Terciario'),
    ], string='Tipo:', required=True)
    peso = fields.Float(string='Peso:', required=True, help ="El numero a ingresar representara el peso en Kg.")
    material = fields.Char(string='Material:', required=True)

    _sql_constraints = [
        ('unique_custom_id', 'UNIQUE(custom_id)', 'El ID debe ser único.')
    ]