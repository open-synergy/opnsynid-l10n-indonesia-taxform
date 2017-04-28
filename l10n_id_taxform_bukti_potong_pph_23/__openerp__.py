# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Bukti Potong PPh 23",
    "version": "8.0.1.2.1",
    "category": "localization",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_id_taxform_bukti_potong_pph_common",
    ],
    "data": [
        "data/l10n_id_bukti_potong_type.xml",
        "views/bukti_potong_pph_23_in_views.xml",
        "views/bukti_potong_pph_23_out_views.xml",
    ],
}
