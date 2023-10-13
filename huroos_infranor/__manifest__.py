# -*- coding: utf-8 -*-
{
    'name': "Huroos Infranor",
    'summary': "Modulo custom per Infranor",
    'description': "Modulo custom per Infranor",
    'author': "Huroos srl",
    'website': "https://www.huroos.com/",
    'category': 'Sales',
    'version': '16.0.3',

    'depends': [
        'base',
        'sale_management',
        'purchase',
        'huroos_data_iva',
        'l10n_it_delivery_note',
        'huroos_reports_ddt',
        'l10n_it_fatturapa_out',
        'huroos_country_region'
    ],

    'data': [
        'security/vat_registry_security.xml',
        'security/ir.model.access.csv',
        'views/order_line_filters.xml',
        'views/account_journal_view.xml',
        'views/account_view.xml',
        'views/date_iva.xml',
        'views/res_partner.xml',
        'views/res_partner_budget.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
        'views/stock_delivery_note.xml',
        'views/huroos_dashboard.xml',
        'views/stock_picking_form.xml',
        'wizard/wizard_posizione.xml',
        'reports/external_layout_custom.xml',
        'reports/sale_order_template.xml',
        'reports/stock_delivery_note_template.xml',
        'views/product_product.xml',
    ]
}
