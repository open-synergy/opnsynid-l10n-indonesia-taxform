# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia's Taxform - Coretax PPh 21 Withholding XML from Payslip Batch",
    "version": "14.0.1.0.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
        "Michael Viriyananda <viriyananda.michael@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_hr_payroll_batch",
        "ssi_l10n_id_taxform_pph_21_payslip",
        "report_xml",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/coretax_bupot_21_report.xml",
        "reports/coretax_bupot_21_template.xml",
        "wizards/payslip_batch_coretax_export_views.xml",
        "views/hr_payslip_batch_views.xml",
    ],
    "demo": [],
}
