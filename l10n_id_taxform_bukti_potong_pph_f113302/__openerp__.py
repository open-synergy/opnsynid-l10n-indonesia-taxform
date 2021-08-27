# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Bukti Potong PPh 21  Final (F.1.1.33.02)",
    "version": "8.0.1.2.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
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
        "data/base_workflow_policy_pph_f113302_out_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "views/bukti_potong_pph_f113302_out_views.xml",
    ],
}
