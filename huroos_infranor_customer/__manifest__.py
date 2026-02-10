{
    'name': "Huroos | Infranor Customer",
    'summary': "Estende anagrafica clienti con campi tecnici su motori, azionamenti, riduttori, bus di campo",
    'description': """Estende anagrafica clienti con campi tecnici su motori, azionamenti, riduttori, bus di campo""",
    'author': "Huroos srl",
    'images': ['static/description/icon.png'],
    'website': 'https://huroos.com',
    'license': 'LGPL-3',
    'category': 'custom',
    'version': '0.1',
    'depends': [
        'base',
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/menu_root.xml',

        'views/bus_type.xml',
        'views/feedback_type.xml',
        'views/motor_type_linear.xml',
        'views/motor_type_rotary.xml',
        'views/protection_level.xml',
        'views/reducer_type.xml',
        'views/res_partner.xml',
        'views/security_function.xml',
        'views/voltage_type.xml',
    ],
    'assets': {},
}
