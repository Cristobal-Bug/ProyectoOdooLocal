from odoo import models, fields, api
from odoo.exceptions import UserError


class Producto(models.Model):
    _name = 'proyecto_odoo.producto'
    _description = 'Modelo de Producto'

    # Campos principales del producto
    name = fields.Char(string='Nombre Producto', required=True)
    codigo = fields.Char(string='Código Producto', required=True)
    periodo_id = fields.Many2one('proyecto_odoo.periodo', string='Periodo', required=True)
    partes_ids = fields.Many2many('proyecto_odoo.parte', string='Listado de Partes')

    # Campos calculados
    peso_total = fields.Float(string="Peso Total", compute="_compute_peso_total", store=True)
    descripcion_peso_total = fields.Char(string="Descripción del Peso Total", compute="_compute_descripcion_peso_total")

    # Métodos de cálculo
    @api.depends('partes_ids.peso')
    def _compute_peso_total(self):
        """Calcula el peso total sumando el peso de todas las partes asociadas."""
        for record in self:
            record.peso_total = sum(parte.peso for parte in record.partes_ids)

    @api.depends('peso_total')
    def _compute_descripcion_peso_total(self):
        """Genera una descripción del peso total."""
        for record in self:
            record.descripcion_peso_total = f"Peso Total Calculado (Kg) = {record.peso_total}"

    # Metodo para calcular el peso total manualmente (si se requiere en acciones específicas)
    def calcular_peso_total(self):
        for record in self:
            if record.partes_ids:
                peso_total = sum(parte.peso for parte in record.partes_ids)
                record.peso_total = peso_total
                return f"Peso total calculado: {peso_total} kg"
            else:
                return "No hay partes asociadas a este producto."

    # Metodo para filtrar productos por peso mínimo
    def filtrar_productos_por_peso(self, peso_minimo):
        if peso_minimo <= 0:
            raise UserError("Por favor, ingrese un peso mínimo válido mayor a 0.")

        # Buscar productos con peso total mayor o igual al peso mínimo
        productos_filtrados = self.search([('peso_total', '>=', peso_minimo)])
        if not productos_filtrados:
            raise UserError(f"No se encontraron productos con peso mayor o igual a {peso_minimo} kg.")

        # Mostrar los productos filtrados en una vista de lista
        return {
            'type': 'ir.actions.act_window',
            'name': 'Productos Filtrados',
            'res_model': 'proyecto_odoo.producto',
            'view_mode': 'list',
            'domain': [('id', 'in', productos_filtrados.ids)],
            'context': self.env.context,
        }

    # Metodo para abrir el wizard y mostrar las partes y sus tipos

    def obtener_partes_y_tipos(self):
        """Muestra las partes y sus tipos asociadas a un producto en un wizard."""
        for producto in self:
            # Imprimir el contenido de partes_ids para debug
            if not producto.partes_ids:
                raise UserError("Este producto no tiene partes asociadas.")

            # Asegurarse de que 'partes_ids' contiene datos
            partes_info = []
            for parte in producto.partes_ids:
                # Verificamos que 'parte' tiene los campos 'name' y 'tipo'
                if parte.name and parte.tipo:
                    partes_info.append(f"Parte: {parte.name}, Tipo: {parte.tipo}")
                else:
                    partes_info.append(f"Parte sin nombre o tipo")

            # Si no hay información de partes, mostrar un mensaje alternativo
            if not partes_info:
                raise UserError("Este producto no tiene partes con nombre o tipo definidos.")

            mensaje = "\n".join(partes_info)

            # Abrir el wizard para mostrar la información
            return {
                'type': 'ir.actions.act_window',
                'name': f"Partes del producto: {producto.name}",
                'res_model': 'wizard.mensaje.producto',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_message': mensaje,
                },
            }

    class WizardMensajeProducto(models.TransientModel):
        _name = 'wizard.mensaje.producto'
        _description = 'Mensaje de Partes del Producto'

        # Campo para mostrar el mensaje
        message = fields.Text(string="Detalles del Producto", readonly=True)