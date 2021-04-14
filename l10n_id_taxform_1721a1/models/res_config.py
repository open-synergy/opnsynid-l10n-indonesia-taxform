# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResConfig(models.TransientModel):
    _name = "l10n_id.taxform_1721a1_config_setting"
    _inherit = "res.config.settings"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    taxform_1721a1_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Taxform 1721 A1",
        comodel_name="res.groups",
        related="company_id.taxform_1721a1_confirm_grp_ids",
    )
    taxform_1721a1_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Taxform 1721 A1",
        comodel_name="res.groups",
        related="company_id.taxform_1721a1_restart_approval_grp_ids",
    )
    taxform_1721a1_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Taxform 1721 A1",
        comodel_name="res.groups",
        related="company_id.taxform_1721a1_cancel_grp_ids",
    )
    taxform_1721a1_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Taxform 1721 A1",
        comodel_name="res.groups",
        related="company_id.taxform_1721a1_restart_grp_ids",
    )
    python_code_1721a1_penghasilan_01 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 01 - Gaji/Pensiun THT/JHT",
        related="company_id.python_code_1721a1_penghasilan_01",
    )
    python_code_1721a1_penghasilan_02 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 02 - \
            Tunjangan PPh",
        related="company_id.python_code_1721a1_penghasilan_02",
    )
    python_code_1721a1_penghasilan_03 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 03 - \
            Tunjangan Lainnya Uang Lembur dsb",
        related="company_id.python_code_1721a1_penghasilan_03",
    )
    python_code_1721a1_penghasilan_04 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 04 - \
            Honorarium dan Imbalan Lain Sejenisnya",
        related="company_id.python_code_1721a1_penghasilan_04",
    )
    python_code_1721a1_penghasilan_05 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 05 - \
            Premi Asuransi Yang Dibayar Pemberi Kerja",
        related="company_id.python_code_1721a1_penghasilan_05",
    )
    python_code_1721a1_penghasilan_06 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 06 - \
            Penerimaan dalam Bentuk Natura",
        related="company_id.python_code_1721a1_penghasilan_06",
    )
    python_code_1721a1_penghasilan_07 = fields.Text(
        string="Python Code for 1721 A1 Penghasilan 07 - \
            Tantiem, Bonus, Gratifikasi, THR",
        related="company_id.python_code_1721a1_penghasilan_07",
    )
    python_code_1721a1_pengurang_10 = fields.Text(
        string="Python Code for 1721 A1 Pengurang 10 - \
            Iuran Pensiun atau THT/JHT",
        related="company_id.python_code_1721a1_pengurang_10",
    )
    python_code_1721a1_perhitungan_13 = fields.Text(
        string="Python Code for 1721 A1 Perhitungan 13 - \
            Penghasilan Netto Masa Sebelumnya",
        related="company_id.python_code_1721a1_perhitungan_13",
    )
    python_code_1721a1_perhitungan_18 = fields.Text(
        string="Python Code for 1721 A1 Perhitungan 18 - \
            PPh 21 Yang Dipotong Masa Sebelumnya",
        related="company_id.python_code_1721a1_perhitungan_18",
    )
    python_code_1721a1_perhitungan_20 = fields.Text(
        string="Python Code for 1721 A1 Perhitungan 20 - \
            PPh 21 dan 26 Yang Telah Dilunasi",
        related="company_id.python_code_1721a1_perhitungan_20",
    )
