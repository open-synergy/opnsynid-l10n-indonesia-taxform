# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Bukti Potong PPh 23",
    "version": "8.0.1.5.0",
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
        "security/ir.model.access.csv",
        "data/l10n_id_bukti_potong_type.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_pph_23_in_data.xml",
        "data/base_workflow_policy_pph_23_out_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "views/bukti_potong_pph_23_in_views.xml",
        "views/bukti_potong_pph_23_out_views.xml",
    ],
}
