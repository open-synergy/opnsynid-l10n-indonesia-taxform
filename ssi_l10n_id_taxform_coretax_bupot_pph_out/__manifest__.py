# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia's Taxform - Coretax Bukti Potong PPh Out XML Export",
    "version": "14.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_l10n_id_taxform_bukti_potong_pph_mixin",
        "ssi_l10n_id_taxform_bukti_potong_pph_f113306",
    ],
    "data": [
        "reports/coretax_bupot_pph_out_template.xml",
        "views/bukti_potong_pph_mixin_views.xml",
    ],
    "demo": [],
}
