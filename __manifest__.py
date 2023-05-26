{
    'name': 'NXC Sales Checklist Addon',
    'version': '15.0',
    'category': 'sales',
    'summary': 'Adds feasibility review checklist, contract review checklist, and a status indicator to the Sale Order model.',
    'description': 'This custom module was developed for Next Chapter Manufacturing to prompt users with checklists on Quotations and Sales Orders. The addon includes stop-gates to prevent order confirmation prior to checklists completion.',
    'author': 'Hayden McCarthy',
    'website': 'https://www.nxcmfg.com',
    'license': 'AGPL-3',
    'depends': ['sale'],
    'data': [
        'views/view_nxc_sales_checklist_order_form.xml',
    ],
    'installable': True,
    'auto_install': False,
}

