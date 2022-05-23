# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia's Taxform",
    "version": "14.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/tax_period_views.xml",
        "views/taxform_objek_pajak_views.xml",
        "data/taxform_objek_pajak_data.xml",
    ],
}
