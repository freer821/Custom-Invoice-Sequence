{
    "name": "Custom Invoice Sequence",
    "version": "18.0.1.0.0",
    "summary": "Allow companies to customize invoice numbering via dedicated sequences.",
    "category": "Accounting/Accounting",
    "author": "tofu-lee",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "data/ir_sequence_data.xml",
        "views/res_company_views.xml",
        "views/ir_sequence_views.xml"
    ],
    "application": False,
    "installable": True
}
