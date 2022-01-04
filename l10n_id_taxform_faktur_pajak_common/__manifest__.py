# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Indonesia - Faktur Pajak Common Feature",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "category": "Localization",
    "depends": [
        "l10n_id_taxform",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/faktur_pajak_transaction_type_data",
        "menu.xml",
        "views/faktur_pajak_transaction_type_views.xml",
        "views/account_invoice_views.xml",
        "views/account_invoice_line_views.xml",
        "views/nomor_seri_faktur_pajak_views.xml",
    ],
    "installable": True,
}
