# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class BuktiPotongPPhf113308OutLine(models.Model):
    _name = "l10n_id.bukti_potong_pph_f113308_out_line"
    _inherit = "l10n_id.bukti_potong_pph_line_mixin"
    _description = "Bukti Potong PPh 26 (f.1.1.33.08) Out Line"

    bukti_potong_id = fields.Many2one(
        comodel_name="l10n_id.bukti_potong_pph_f113308_out",
    )
    income_move_line_ids = fields.Many2many(
        relation="rel_bukpot_f113308_out_line_2_income_move",
        column1="bukpot_line_id",
        column2="account_move_id",
    )
