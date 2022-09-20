# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Mixin Feature for Bukti Potong PPh",
    "version": "11.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "account",
        "ssi_master_data_mixin",
        "ssi_transaction_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "l10n_id_taxform",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data_decimal_precision.xml",
        "menu.xml",
        "views/bukti_potong_pph_type_views.xml",
        "views/bukti_potong_pph_mixin_views.xml",
    ],
}
