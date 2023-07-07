# -*- coding: utf-8 -*-
{
    'name': "Huroos Infranor",
    'summary': "Modulo custom per Infranor",
    'description': "Modulo custom per Infranor",
    'author': "Huroos srl",
    'website': "https://www.huroos.com/",
    'category': 'Sales',
    'version': '16.0.0.1',

    'depends': ['base', 'sale_management', 'purchase', 'huroos_data_iva'],

    'data': [
        'security/vat_registry_security.xml',
        'security/ir.model.access.csv',

        'views/account_journal_view.xml',
        'views/account_view.xml',
        'views/date_iva.xml',
        'views/res_partner.xml',
        'views/res_partner_budget.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',

        'reports/sale_order_template.xml'
    ]
}
