{
    'name': 'Proyecto Odoo',
    'version': '1.0',
    'summary': 'Módulo de prueba para Odoo',
    'author': 'Cristobal Reyes Lucero',
    'category': 'Productos',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/producto_views.xml',
        'views/periodo_views.xml',
        'views/parte_views.xml',
        'views/producto_menu.xml',
        'views/wizard_view.xml'
    ],
    'installable': True,
    'application': True,
}