# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Bukti Potong PPh 23 (f.1.33.06)",
    "version": "11.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_l10n_id_taxform_bukti_potong_pph_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/l10n_id_bukti_potong_type.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "data/account_journal_data.xml",
        "views/bukti_potong_pph_type_views.xml",
        "views/bukti_potong_pph_f113306_in_views.xml",
        "views/bukti_potong_pph_f113306_out_views.xml",
    ],
    "demo": [
        "demo/account_journal_demo.xml",
        "demo/account_account_demo.xml",
        "demo/account_tax_demo.xml",
        "demo/l10n_id_bukti_potong_type_demo.xml",
    ],
}
