# -*- coding: utf-8 -*-

{
    'name': 'Tran Duc Anh Glass Merchant',
    'version': '15.0.0.1.0',
    'category': 'Hidden',
    'sequence': 9876,
    'summary': 'Tran Duc Anh Glass Store',
    'description': """Manage Glass Store""",
    'depends': ['product', 'field_timepicker'],
    'data': [
        'security/ir.model.access.csv',  

        'views/tda_products_template.xml',
        'views/tda_product_views.xml',
        'views/tda_info_views.xml',
        'views/tda_address_views.xml',
        'views/tda_projects_category_views.xml',
        'views/tda_projects_view.xml',
        'views/tda_advisory_request_views.xml',
        'views/tda_feng_shui_views.xml',
        'views/menu_item.xml',
    ],
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js',
            '/tda_glass_merchant/static/src/xml/custom_dashboard.xml',
            '/tda_glass_merchant/static/src/js/custom_dashboard.js',
            '/tda_glass_merchant/static/src/css/dashboard_css.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
