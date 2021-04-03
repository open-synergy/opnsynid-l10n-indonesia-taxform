# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = [
        "res.company",
    ]

    python_code_1721a1_penghasilan_01 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 01 - Gaji/Pensiun THT/JHT",
        default="result = 0.0",
    )
    python_code_1721a1_penghasilan_02 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 02 - \
            Tunjangan PPh",
        default="result = 0.0",
    )
    python_code_1721a1_penghasilan_03 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 03 - \
            Tunjangan Lainnya Uang Lembur dsb",
        default="result = 0.0",
    )
    python_code_1721a1_penghasilan_04 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 04 - \
            Honorarium dan Imbalan Lain Sejenisnya",
        default="result = 0.0",
    )
    python_code_1721a1_penghasilan_05 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 05 - \
            Premi Asuransi Yang Dibayar Pemberi Kerja",
        default="result = 0.0",
    )
    python_code_1721a1_penghasilan_06 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 06 - \
            Penerimaan dalam Bentuk Natura",
        default="result = 0.0",
    )
    python_code_1721a1_penghasilan_07 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 07 - \
            Tantiem, Bonus, Gratifikasi, THR",
        default="result = 0.0",
    )
    python_code_1721a1_pengurang_10 = fields.Text(
        string="Python Code for 1721 A1 Pengurang 10 - \
            Iuran Pensiun atau THT/JHT",
        default="result = 0.0",
    )
    python_code_1721a1_perhitungan_13 = fields.Text(
        string="Python Code for 1721 A1 Perhitungan 13 - \
            Penghasilan Netto Masa Sebelumnya",
        default="result = 0.0",
    )
    python_code_1721a1_perhitungan_18 = fields.Text(
        string="Python Code for 1721 A1 Perhitungan 18 - \
            PPh 21 Yang Dipotong Masa Sebelumnya",
        default="result = 0.0",
    )
    python_code_1721a1_perhitungan_20 = fields.Text(
        string="Python Code for 1721 A1 Perhitungan 20 - \
            PPh 21 dan 26 Yang Telah Dilunasi",
        default="result = 0.0",
    )
    taxform_1721a1_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Taxform 1721 A1",
        comodel_name="res.groups",
        relation="rel_company_id_confirm_taxform_1721a1",
        column1="company_id",
        column2="group_id",
    )
    taxform_1721a1_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Taxform 1721 A1",
        comodel_name="res.groups",
        relation="rel_company_id_restart_approval_taxform_1721a1",
        column1="company_id",
        column2="group_id",
    )
    taxform_1721a1_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Taxform 1721 A1",
        comodel_name="res.groups",
        relation="rel_company_id_cancel_taxform_1721a1",
        column1="company_id",
        column2="group_id",
    )
    taxform_1721a1_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Taxform 1721 A1",
        comodel_name="res.groups",
        relation="rel_company_id_restart_taxform_1721a1",
        column1="company_id",
        column2="group_id",
    )
