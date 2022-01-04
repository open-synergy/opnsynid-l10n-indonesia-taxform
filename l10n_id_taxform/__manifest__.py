# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia's Taxform",
    "version": "11.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia," "PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/tax_period_views.xml",
    ],
}
