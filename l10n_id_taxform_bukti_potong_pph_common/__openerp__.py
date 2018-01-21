# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Common Feature for Bukti Potong",
    "version": "8.0.5.0.0",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mail",
        "l10n_id_taxform_period",
        "base_amount_to_text"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data_decimal_precision.xml",
        "views/l10n_id_taxform_bukti_potong_pph_type_views.xml",
        "views/bukti_potong_pph_views.xml",
    ],
}
