# -*- coding: utf-8 -*-

{
    'name': 'Transport Package Report',
    'version': '17.0.0.0',
    'category': '',
    "license": "OPL-1",
    'summary': 'Transport Package Report',
    'description': """ Transport Package Report
use for submit packaging details """,
    'author': 'ERP Partner OÜ',
    'support': 'info@erppartner.ee',
    'maintainer': 'ERP Partner OÜ <info@erppartner.ee>',
    'website': 'https://www.erppartner.ee',
    'depends': ['stock'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/stock_picking.xml"
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
