# -*- coding: utf-8 -*-
{
    'name': 'SD Dashboard',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': """ """,
    'author': 'Arash Homayounfar',
    'company': 'Giladoo',
    'maintainer': 'Giladoo',
    'website': "https://www.giladoo.com",
    'installable': True,
    'auto_install': False,
    'application': False,
    'depends': ['base', 'hr',],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/hr_employee_views.xml',
        # 'data/document_type_data.xml',
    ],
'assets': {
        'web.assets_backend':[
            'sd_hr_dashboard/static/src/components/**/*'
        ],

    },
    'demo': [

    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
}
