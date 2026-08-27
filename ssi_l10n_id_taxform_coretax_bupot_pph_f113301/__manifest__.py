# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Indonesia's Taxform - Coretax Bukti Potong PPh 21/26 f.1.1.33.01"
    " Out XML Export",
    "version": "14.0.1.1.0",
    "category": "localization",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_l10n_id_taxform",
        "ssi_l10n_id_taxform_pph_21",
        "ssi_l10n_id_taxform_bukti_potong_pph_f113301",
        "ssi_l10n_id_taxform_coretax_bupot_pph_out",
        "report_xml",
    ],
    "data": [
        "security/res_groups/l10n_id_taxform_kode_fasilitas_pajak.xml",
        "security/res_groups/l10n_id_taxform_jenis_dokumen_referensi.xml",
        "security/ir_model_access/l10n_id_taxform_kode_fasilitas_pajak.xml",
        "security/ir_model_access/l10n_id_taxform_jenis_dokumen_referensi.xml",
        "data/taxform_objek_pajak_data.xml",
        "views/taxform_objek_pajak_views.xml",
        "views/taxform_kode_fasilitas_pajak_views.xml",
        "views/taxform_jenis_dokumen_referensi_views.xml",
        "reports/coretax_bupot_pph_f113301_out_template.xml",
        "reports/coretax_bupot_pph_f113301_out_report.xml",
        "views/bukti_potong_pph_f113301_out_views.xml",
    ],
    "demo": [],
}
