# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia's PPh 21 Taxform",
    "version": "14.0.1.1.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_l10n_id_taxform",
        "account",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "data/ptkp_category_data.xml",
        "menu.xml",
        "views/ptkp_category_views.xml",
        "views/ptkp_views.xml",
        "views/pph_21_biaya_jabatan_views.xml",
        "views/pph_21_npwp_rate_modifier_views.xml",
        "views/pph_21_rate_views.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [
        "demo/pph_21_biaya_jabatan_demo.xml",
        "demo/pph_21_npwp_rate_modifier_demo.xml",
        "demo/pph_21_rate_demo.xml",
        "demo/ptkp_demo.xml",
    ],
}
