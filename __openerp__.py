
{
    'name': 'Accounting Reports',
    'version': '1.0.0',
    'category': 'hospital service',
    'description': """
This module is to configure modules related to an association.
==============================================================

It installs the profile for associations to manage events, registrations, memberships, 
membership products (schemes).
    """,
    'author': 'BLF Team',
    'depends': ['sale'],
    'data': [
        'wizard/cash_debit.xml',
        'wizard/bank_debit.xml',
        'wizard/trial_balance_view.xml',
        'report/report_cash_debit.xml',
        'report/report_bank_debit.xml',
        'report/report_trial_balance.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'website': 'https://www.mufti.com'
}
