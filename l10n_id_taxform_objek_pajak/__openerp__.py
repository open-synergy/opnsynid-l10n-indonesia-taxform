# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia - Tax Form Objek Pajak",
    "version": "8.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "l10n_id_taxform",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/l10n_id_taxform_objek_pajak_data.xml",
        "views/l10n_id_taxform_objek_pajak_views.xml",
    ],
}
