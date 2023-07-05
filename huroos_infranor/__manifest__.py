# -*- coding: utf-8 -*-
{
    'name': "Huroos Infranor",
    'summary': "Modulo custom per Infranor",
    'description': "Modulo custom per Infranor",
    'author': "Huroos srl",
    'website': "https://www.huroos.com/",
    'category': 'Sales',
    'version': '16.0.0.1',


    'depends': ['base', 'sale_management'],

    'data': [
        'security/ir.model.access.csv',

        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/res_partner_budget.xml',
        'views/sale_order_line.xml'
    ]
}
